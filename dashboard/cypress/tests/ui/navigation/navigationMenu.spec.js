import sideBar from "../../../locators/sideBarLocators";
import { localeContent as globalBlocklistLc } from "../../../locators/globalBlocklist";
import { localeContent as commonLc } from "../../../locators/common";

describe("Navigation menu items", () => {
	beforeEach(() => {
		cy.loginGlobalUserProgrammatically();
	});

	describe("Global Blocklist permissions", () => {
		it("user with the VIEW_SETTINGS_MENU and VIEW_GLOBAL_BLOCKLIST_MENU permissions should be able to access Global Blocklist form via the Admin menu", () => {
			// Visit home page
			cy.visit("/");
			// Open Admin Menu
			cy.clickElement(sideBar.navigationMenuButtonAdmin);
			cy.clickElement(sideBar.navigationItemGlobalBlocklist);
			// We should be on the Global Blocklist form screen
			cy.findByRole("heading", { name: globalBlocklistLc.PAGE_HEADER });
		});

		it("user with the VIEW_SETTINGS_MENU but without the VIEW_GLOBAL_BLOCKLIST_MENU permissions should not be able to access Global Blocklist form", () => {
			const USERNAME = `automation-test-navigationMenu-no-blocklist-permission@user.com`;

			cy.createUserWithPermissions({
				userRoleName: `Automation_Test_Role_navigationMenu_no_blocklist_permission`,
				username: USERNAME,
				permissionsToEnable: [
					// Necessary to load reporting dashboard homepage
					"AUTHENTICATE_MANAGER",
					"VIEW_MANAGE_DASHBOARD",
					"VIEW_NETWORK_REPORT",
					"VIEW_REPORTING_MENU",
					// Test Specific permissions
					"VIEW_SETTINGS_MENU",
					"VIEW_AUDIENCE_MENU",
				],
			});

			cy.loginProgrammatically({
				username: USERNAME,
			});

			// Visit home page
			cy.visit("/");
			// Open Admin Menu
			cy.clickElement(sideBar.navigationMenuButtonAdmin);
			// Link to route should not be rendered
			cy.verifyElementsNotExist(sideBar.navigationItemGlobalBlocklist);

			// Attempt to visit the route directly
			cy.visit("/dashboard/global-blocklist");

			// We should be redirected to the 403 page
			cy.findByRole("heading", { name: commonLc.ACCESS_DENIED_PAGE_HEADING }).should("exist");
			cy.findByRole("heading", { name: globalBlocklistLc.PAGE_HEADER }).should("not.exist");
		});
	});
});
