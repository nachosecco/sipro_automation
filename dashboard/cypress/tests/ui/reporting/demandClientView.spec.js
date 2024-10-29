import { localeContent as lc } from "../../../locators/reportingLocators.js";
import { getHomepagePermissions } from "../../../utils/getBasePermissions.js";

describe("Demand Client users should see alternate labels for certain metrics", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("when report type is campaign or network, Gross Revenue should appear as Gross Spend", () => {
		// Create a demand client user who only has access to the Gross Revenue aka gross spend metric for campaign and network reports
		const USERNAME = `demand-client-user@automation.com`;
		cy.createUserWithPermissions({
			userRoleName: `demand_client_user`,
			username: USERNAME,
			permissionsToEnable: [
				// Grant base permissions as well as ability to view network reporting
				...getHomepagePermissions(),
				// Grant access to campaign reports
				"VIEW_CAMPAIGN_REPORT",
				"VIEW_NETWORK_REPORT",
				// Grant access to only gross revenue aka gross spend
				"VIEW_NETWORK_REPORT_METRIC_GROSS_REVENUE",
				"VIEW_CAMPAIGN_REPORT_METRIC_GROSS_REVENUE",
			],
			userModelExtension: {
				isDemandClient: true,
			},
		});

		// Login as the demand client user
		cy.loginProgrammatically({
			username: USERNAME,
		});

		function verifyGrossSpendLabels() {
			// Verify that column header is correct
			cy.findByRole("columnheader", { name: `${lc.DEMAND_CLIENT_METRIC_LABELS.GROSS_REVENUE} ($)` }).should(
				"be.visible"
			);
			// Verify that KPI label is correct
			cy.findByTestId("grossrevenue")
				.should("be.visible")
				.should("have.text", lc.DEMAND_CLIENT_METRIC_LABELS.GROSS_REVENUE);
			// Verify that chart metric label is correct
			cy.findByRole("button", { name: lc.DEMAND_CLIENT_METRIC_LABELS.GROSS_REVENUE }).click();
			cy.findByRole("option", { name: lc.DEMAND_CLIENT_METRIC_LABELS.GROSS_REVENUE }).should("be.visible");
			// Close the menu
			cy.get("body").type("{esc}");
			// Navigate to Scheduled Reports to make sure labels are correct there as well
			cy.findByRole("link", { name: lc.SCHEDULE_REPORTS_BUTTON }).click();
			// Open Data Tab
			cy.findByRole("tab", { name: lc.SCHEDULE_REPORTS_TAB_LABEL.DATA }).click();
			// Gross Spend metric should be selected
			cy.findByRole("button", { name: lc.DEMAND_CLIENT_METRIC_LABELS.GROSS_REVENUE }).should("exist");
		}

		// Visit the reporting dashboard - Network Reporting
		cy.visit("/dashboard/reporting?reportType=network");
		// Use the common function to verify the labels
		verifyGrossSpendLabels();

		// Visit the reporting dashboard - Campaign Reporting
		cy.visit("/dashboard/reporting?reportType=campaign");
		// Use the common function to verify the labels
		verifyGrossSpendLabels();
	});
});
