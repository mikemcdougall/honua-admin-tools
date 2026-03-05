/**
 * Vue components and composables for Honua admin tools
 */

export interface VueAdminProps {
  client: any; // Would be typed properly
  onServiceChange?: (serviceId: string) => void;
}

// Placeholder for Vue integration
export const HonuaAdminPlugin = () => {
  throw new Error('Vue plugin not implemented yet');
};

export const useHonuaAdmin = () => {
  throw new Error('Vue composables not implemented yet');
};