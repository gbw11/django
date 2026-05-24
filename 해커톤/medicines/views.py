from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Medicine, Interaction, PersonalizedDosage


def index(request):
    popular = Medicine.objects.all()[:4]
    return render(request, 'medicines/index.html', {'popular': popular})


def search(request):
    query = request.GET.get('q', '')
    results = []
    if query:
        results = Medicine.objects.filter(
            Q(name__icontains=query) |
            Q(usage__icontains=query) |
            Q(ingredients__name__icontains=query)
        ).distinct()
    return render(request, 'medicines/search.html', {
        'results': results, 'query': query
    })


def medicine_detail(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    ingredients = medicine.medicineingredient_set.select_related('ingredient')

    interactions = Interaction.objects.filter(
        Q(medicine_a=medicine) | Q(medicine_b=medicine)
    ).select_related('medicine_a', 'medicine_b')

    # ── 개인화 처리 ──
    profile = None
    personalized = None
    age_group = 'adult'
    profile_complete = False

    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            # 나이가 입력된 경우에만 완성된 프로필로 간주
            profile_complete = profile.age is not None
            if profile_complete:
                age_group = profile.get_age_group()
                try:
                    personalized = medicine.personalized_dosages.get(age_group=age_group)
                except PersonalizedDosage.DoesNotExist:
                    personalized = None
        except Exception:
            profile = None

    risk_level, risk_reasons = assess_risk(medicine, interactions, profile)

    return render(request, 'medicines/detail.html', {
        'medicine': medicine,
        'ingredients': ingredients,
        'interactions': interactions,
        'profile': profile,
        'profile_complete': profile_complete,
        'personalized': personalized,
        'age_group': age_group,
        'risk_level': risk_level,
        'risk_reasons': risk_reasons,
        'current_path': request.path,
    })


def assess_risk(medicine, interactions, profile):
    reasons = []
    score = 0

    forbidden = [i for i in interactions if i.level == 'FORBIDDEN']
    caution   = [i for i in interactions if i.level == 'CAUTION']
    if forbidden:
        score += 3
        reasons.append(f"⛔ 병용 금기 상호작용 {len(forbidden)}건 존재")
    if caution:
        score += 1
        reasons.append(f"⚠️ 병용 주의 상호작용 {len(caution)}건 존재")

    if profile:
        if profile.is_pregnant and '임신' in medicine.contraindications:
            score += 3
            reasons.append("⛔ 임산부 금기 약품입니다")
        if profile.is_breastfeeding:
            score += 1
            reasons.append("⚠️ 수유 중에는 복용 전 약사 확인 권장")
        if profile.age:
            if profile.age >= 65 and '노인' in medicine.precautions:
                score += 2
                reasons.append("⚠️ 65세 이상 고령자 주의 약품입니다")
            if profile.age < 12:
                score += 2
                reasons.append("⚠️ 소아(12세 미만) 복용 주의")
            if profile.age < 2:
                score += 2
                reasons.append("⛔ 영아에게 임의 투여 금지")
        if profile.conditions:
            cond_list = [c.strip() for c in profile.conditions.split(',')]
            for cond in cond_list:
                if cond and cond in medicine.contraindications:
                    score += 2
                    reasons.append(f"⛔ 지병({cond})으로 인한 금기 해당 가능")

        # 복용 중인 약과의 상호작용 추가 검사
        current_meds = profile.current_medicines.all()
        for cur_med in current_meds:
            if cur_med.pk != medicine.pk:
                cross = Interaction.objects.filter(
                    Q(medicine_a=medicine, medicine_b=cur_med) |
                    Q(medicine_a=cur_med, medicine_b=medicine)
                ).first()
                if cross:
                    if cross.level == 'FORBIDDEN':
                        score += 3
                        reasons.append(f"⛔ 현재 복용 중인 '{cur_med.name}'과 병용 금기")
                    else:
                        score += 1
                        reasons.append(f"⚠️ 현재 복용 중인 '{cur_med.name}'과 병용 주의")

    if not reasons:
        reasons.append("✅ 현재 입력된 정보 기준 특이 위험요소 없음")

    if score >= 3:
        return 'HIGH', reasons
    elif score >= 1:
        return 'MEDIUM', reasons
    return 'LOW', reasons


def analyze(request):
    all_medicines = Medicine.objects.all()
    result = None

    if request.method == 'POST':
        ids = request.POST.getlist('medicine_ids')
        selected = Medicine.objects.filter(pk__in=ids)
        interactions = []
        meds = list(selected)
        for i in range(len(meds)):
            for j in range(i + 1, len(meds)):
                found = Interaction.objects.filter(
                    Q(medicine_a=meds[i], medicine_b=meds[j]) |
                    Q(medicine_a=meds[j], medicine_b=meds[i])
                )
                interactions.extend(found)

        has_forbidden = any(i.level == 'FORBIDDEN' for i in interactions)
        has_caution   = any(i.level == 'CAUTION'   for i in interactions)
        overall = 'HIGH' if has_forbidden else ('MEDIUM' if has_caution else 'LOW')
        result = {'selected': selected, 'interactions': interactions, 'overall': overall}

    return render(request, 'medicines/analyze.html', {
        'all_medicines': all_medicines, 'result': result
    })