from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import Medicine, Interaction, UserProfile

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
    return render(request, 'medicines/search.html', {'results': results, 'query': query})

def medicine_detail(request, pk):
    medicine = get_object_or_404(Medicine, pk=pk)
    ingredients = medicine.medicineingredient_set.select_related('ingredient')

    # 상호작용 조회 (양방향)
    interactions = Interaction.objects.filter(
        Q(medicine_a=medicine) | Q(medicine_b=medicine)
    ).select_related('medicine_a', 'medicine_b')

    # 사용자 프로필 (세션 기반)
    profile = None
    session_key = request.session.session_key
    if session_key:
        profile = UserProfile.objects.filter(session_key=session_key).first()

    # 위험도 판단
    risk_level, risk_reasons = assess_risk(medicine, interactions, profile)

    return render(request, 'medicines/detail.html', {
        'medicine': medicine,
        'ingredients': ingredients,
        'interactions': interactions,
        'profile': profile,
        'risk_level': risk_level,
        'risk_reasons': risk_reasons,
    })

def assess_risk(medicine, interactions, profile):
    """위험도를 LOW / MEDIUM / HIGH 로 판단"""
    reasons = []
    score = 0

    # 병용 금기 확인
    forbidden = [i for i in interactions if i.level == 'FORBIDDEN']
    caution = [i for i in interactions if i.level == 'CAUTION']
    if forbidden:
        score += 3
        reasons.append(f"⛔ 병용 금기 상호작용 {len(forbidden)}건 존재")
    if caution:
        score += 1
        reasons.append(f"⚠️ 병용 주의 상호작용 {len(caution)}건 존재")

    # 사용자 상태 기반 판단
    if profile:
        if profile.is_pregnant and '임신' in medicine.contraindications:
            score += 3
            reasons.append("⛔ 임산부 금기 약품입니다")
        if profile.age and profile.age >= 65 and '노인' in medicine.precautions:
            score += 2
            reasons.append("⚠️ 65세 이상 고령자 주의 약품입니다")
        if profile.age and profile.age < 12:
            score += 2
            reasons.append("⚠️ 소아(12세 미만) 복용 주의")

    if score >= 3:
        return 'HIGH', reasons
    elif score >= 1:
        return 'MEDIUM', reasons
    else:
        reasons.append("✅ 현재 정보 기준 특이 위험요소 없음")
        return 'LOW', reasons

def analyze(request):
    """약 + 약 상호작용 분석 페이지"""
    all_medicines = Medicine.objects.all()
    result = None

    if request.method == 'POST':
        ids = request.POST.getlist('medicine_ids')
        selected = Medicine.objects.filter(pk__in=ids)
        interactions = []
        meds = list(selected)
        for i in range(len(meds)):
            for j in range(i+1, len(meds)):
                found = Interaction.objects.filter(
                    Q(medicine_a=meds[i], medicine_b=meds[j]) |
                    Q(medicine_a=meds[j], medicine_b=meds[i])
                )
                interactions.extend(found)

        has_forbidden = any(i.level == 'FORBIDDEN' for i in interactions)
        has_caution = any(i.level == 'CAUTION' for i in interactions)
        overall = 'HIGH' if has_forbidden else ('MEDIUM' if has_caution else 'LOW')

        result = {
            'selected': selected,
            'interactions': interactions,
            'overall': overall,
        }

    return render(request, 'medicines/analyze.html', {
        'all_medicines': all_medicines,
        'result': result,
    })

def save_profile(request):
    if request.method == 'POST':
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        profile, _ = UserProfile.objects.get_or_create(session_key=session_key)
        profile.age = request.POST.get('age') or None
        profile.gender = request.POST.get('gender', '')
        profile.height = request.POST.get('height') or None
        profile.weight = request.POST.get('weight') or None
        profile.conditions = request.POST.get('conditions', '')
        profile.is_pregnant = 'is_pregnant' in request.POST
        profile.is_breastfeeding = 'is_breastfeeding' in request.POST
        profile.save()
        medicine_ids = request.POST.getlist('current_medicines')
        profile.current_medicines.set(Medicine.objects.filter(pk__in=medicine_ids))
        from django.http import JsonResponse
        return JsonResponse({'status': 'ok'})
    return render(request, 'medicines/profile.html', {
        'all_medicines': Medicine.objects.all()
    })