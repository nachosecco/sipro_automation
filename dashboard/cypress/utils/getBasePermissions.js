// All permissions necessary to load the Application
const basePermissions = ["AUTHENTICATE_MANAGER", "VIEW_MANAGE_DASHBOARD"];

// All permissions necessary to load the homepage
export const getHomepagePermissions = () => [...basePermissions, "VIEW_REPORTING_MENU", "VIEW_NETWORK_REPORT"];

export default () => [...basePermissions];
