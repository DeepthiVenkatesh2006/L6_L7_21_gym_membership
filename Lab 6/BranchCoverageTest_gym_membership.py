import pytest
from gym_membership import membership_cost, can_enter, bmi_category


# ---------- membership_cost ----------
@pytest.mark.parametrize("plan, base", [("monthly", 1500), ("quarterly", 4000), ("yearly", 12000)])
def test_base_price_no_discount(plan, base):
    assert membership_cost(plan, 30, False, False) == base

def test_unknown_plan():
    with pytest.raises(ValueError, match="unknown plan"):
        membership_cost("weekly", 30, False, False)

def test_too_young():
    with pytest.raises(ValueError, match="too young"):
        membership_cost("monthly", 13, False, False)

def test_age_14_boundary_allowed():
    assert membership_cost("monthly", 14, False, False) == 1500

def test_age_59_no_senior_discount():
    assert membership_cost("monthly", 59, False, False) == 1500

def test_age_60_boundary_senior_discount():
    assert membership_cost("monthly", 60, False, False) == 1125

def test_student_discount():
    assert membership_cost("monthly", 20, True, False) == 1350

def test_senior_student_gets_only_senior_discount():
    assert membership_cost("monthly", 65, True, False) == 1125   # elif not taken

def test_trainer_non_yearly():
    assert membership_cost("monthly", 30, False, True) == 3500   # 1500 + 2000

def test_trainer_yearly_rebate():
    assert membership_cost("yearly", 30, False, True) == 13500   # 12000 + 2000 - 500

def test_senior_student_yearly_trainer_combo():
    assert membership_cost("yearly", 65, True, True) == 10500    # 9000 + 2000 - 500


# ---------- can_enter ----------
def test_can_enter():
    assert can_enter(10, True, False, "M") is True

def test_inactive_plan():
    assert can_enter(10, False, False, "M") is False

def test_hour_too_early():
    assert can_enter(4, True, False, "M") is False

def test_hour_too_late():
    assert can_enter(23, True, False, "M") is False

def test_hour_lower_boundary_5_allowed():
    assert can_enter(5, True, False, "M") is True

def test_hour_upper_boundary_22_allowed():
    assert can_enter(22, True, False, "M") is True

def test_women_only_slot_female():
    assert can_enter(10, True, True, "F") is True

def test_women_only_slot_male():
    assert can_enter(10, True, True, "M") is False


# ---------- bmi_category ----------
@pytest.mark.parametrize("h", [0, -1.7])
def test_invalid_height(h):
    with pytest.raises(ValueError, match="invalid height"):
        bmi_category(70, h)

def test_underweight():
    assert bmi_category(45, 1.75) == "underweight"

def test_normal():
    assert bmi_category(65, 1.75) == "normal"

def test_overweight():
    assert bmi_category(85, 1.75) == "overweight"

def test_obese():
    assert bmi_category(100, 1.75) == "obese"

def test_bmi_boundary_18_5_is_normal():
    assert bmi_category(18.5, 1.0) == "normal"

def test_bmi_boundary_25_is_overweight():
    assert bmi_category(25, 1.0) == "overweight"

def test_bmi_boundary_30_is_obese():
    assert bmi_category(30, 1.0) == "obese"
