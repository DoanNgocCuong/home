// XP calculation utilities based on the new system
export interface XPProgress {
  currentXP: number;
  requiredXP: number;
  percentage: number;
  level: number;
}

export interface StreakInfo {
  days: number;
  years: number;
  multiplier: number;
}

// Base XP required for level 1
const BASE_XP = 1000;
const LEVEL_XP_MULTIPLIER = 1.5;

// Streak multipliers based on duration
const STREAK_MULTIPLIERS = {
  '0-30': 1.0,
  '31-90': 1.05,
  '91-365': 1.1,
  '1-3': 1.2,
  '3-5': 1.3,
  '5-7': 1.5,
  '7-10': 1.8,
  '10-15': 2.5,
  '15+': 5.0,
};

// Special milestone bonuses
const MILESTONE_BONUSES: Record<string, number> = {
  '1': 100,
  '3': 300,
  '5': 500,
  '10': 1000,
  '15': 1500,
};

// XP deduction rates based on streak duration
const XP_DEDUCTION_RATES = {
  '0-3': 0.1,
  '3-6': 0.08,
  '6-12': 0.06,
  '1-3': 0.04,
  '3-5': 0.03,
  '5-10': 0.02,
  '10+': 0.01,
};

export const calculateStreakMultiplier = (streakDays: number): number => {
  const years = streakDays / 365;

  if (years >= 15) return STREAK_MULTIPLIERS['15+'];
  if (years >= 10) return STREAK_MULTIPLIERS['10-15'];
  if (years >= 7) return STREAK_MULTIPLIERS['7-10'];
  if (years >= 5) return STREAK_MULTIPLIERS['5-7'];
  if (years >= 3) return STREAK_MULTIPLIERS['3-5'];
  if (years >= 1) return STREAK_MULTIPLIERS['1-3'];
  if (streakDays >= 91) return STREAK_MULTIPLIERS['91-365'];
  if (streakDays >= 31) return STREAK_MULTIPLIERS['31-90'];
  return STREAK_MULTIPLIERS['0-30'];
};

export const calculateXPProgress = (
  baseXP: number,
  streakDays: number = 0,
): XPProgress => {
  let level = 0;
  let totalXP = baseXP;
  let requiredXP = BASE_XP;
  const streakMultiplier = calculateStreakMultiplier(streakDays);

  // Apply streak multiplier to base XP
  totalXP = Math.floor(baseXP * streakMultiplier);

  // Calculate level based on total XP
  while (totalXP >= requiredXP) {
    level++;
    totalXP -= requiredXP;
    requiredXP = Math.floor(BASE_XP * Math.pow(LEVEL_XP_MULTIPLIER, level));
  }

  return {
    currentXP: totalXP,
    requiredXP: requiredXP,
    percentage: (totalXP / requiredXP) * 100,
    level,
  };
};

export const calculateMilestoneBonus = (years: number): number => {
  const yearKey = Math.floor(years).toString();
  return MILESTONE_BONUSES[yearKey] || 0;
};

export const calculateXPDeduction = (
  totalXP: number,
  streakDays: number,
  consecutiveMissedDays: number = 1,
): number => {
  const years = streakDays / 365;
  let deductionRate = 0;

  // Find appropriate deduction rate
  if (years >= 10) deductionRate = XP_DEDUCTION_RATES['10+'];
  else if (years >= 5) deductionRate = XP_DEDUCTION_RATES['5-10'];
  else if (years >= 3) deductionRate = XP_DEDUCTION_RATES['3-5'];
  else if (years >= 1) deductionRate = XP_DEDUCTION_RATES['1-3'];
  else if (streakDays >= 180) deductionRate = XP_DEDUCTION_RATES['6-12'];
  else if (streakDays >= 90) deductionRate = XP_DEDUCTION_RATES['3-6'];
  else deductionRate = XP_DEDUCTION_RATES['0-3'];

  // Apply consecutive missed days multiplier
  let severityMultiplier: number;
  if (consecutiveMissedDays >= 8) {
    severityMultiplier = 3.0;
  } else if (consecutiveMissedDays >= 4) {
    severityMultiplier = 2.0;
  } else if (consecutiveMissedDays >= 3) {
    severityMultiplier = 1.5;
  } else if (consecutiveMissedDays >= 2) {
    severityMultiplier = 1.2;
  } else {
    severityMultiplier = 1.0;
  }

  return Math.floor(totalXP * deductionRate * severityMultiplier);
};
