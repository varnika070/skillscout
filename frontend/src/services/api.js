import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// API functions
export const generateLearningPath = async (targetSkill, currentSkills = []) => {
  const response = await api.post('/generate-path', {
    target_skill_id: targetSkill,
    current_skills: currentSkills,
  });
  return response.data;
};

export const validateTimeline = async (targetSkill, proposedWeeks) => {
  const response = await api.post('/validate-timeline', {
    target_skill_id: targetSkill,
    proposed_weeks: proposedWeeks,
  });
  return response.data;
};

export const getCommunityInsights = async (skillId) => {
  const response = await api.get(`/community-insights/${skillId}`);
  return response.data;
};

export const getAllSkills = async () => {
  const response = await api.get('/skills');
  return response.data;
};

export const getSkillDetails = async (skillId) => {
  const response = await api.get(`/skill/${skillId}`);
  return response.data;
};

export const checkHealth = async () => {
  const response = await api.get('/health');
  return response.data;
};

export default api;