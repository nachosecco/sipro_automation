import { PRIMARY_COLORS } from "../../../fixtures/colors";
import DEFAULT_COMPANY_REQUEST_BODY from "../../../fixtures/defaultCompanyRequestBody";
import locators, { localeContent as lc } from "../../../locators/reportingLocators";
import { createOrUpdateCompany } from "../../../support/companyCommands";
import { convertHexToRGB } from "../../../utils/colorUtils";

const chartContainerTestId = "line-chart-container";

describe("Reporting charts", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("charts show correct revenue metric per type", () => {
		cy.visit("/dashboard/reporting");

		// Setting date range today so that the graph is visible
		cy.clickElement(locators.dateRange);
		cy.clickElement(locators.dateRangeButtonToday);
		// Click on run report button
		cy.clickElement(locators.runReportButton);

		// Network reports should have gross revenue and impressions in the legend
		cy.findByTestId(chartContainerTestId).within(() => {
			// Left Axis
			cy.findByText(lc.METRIC_LABEL.GROSS_REVENUE);
			// Right Axis
			cy.findByText(lc.METRIC_LABEL.IMPRESSIONS);
		});

		// Switch to Campaign
		cy.clickElement(locators.campaignTab);

		// Campaign reports should have gross revenue and impressions in the legend
		cy.findByTestId(chartContainerTestId).within(() => {
			// Left Axis
			cy.findByText(lc.METRIC_LABEL.GROSS_REVENUE);
			// Right Axis
			cy.findByText(lc.METRIC_LABEL.IMPRESSIONS);
		});

		// Switch to RTB
		cy.clickElement(locators.rtbTab);

		// RTB reports should have close revenue and impressions in the legend
		cy.findByTestId(chartContainerTestId).within(() => {
			// Left Axis
			cy.findByText(lc.METRIC_LABEL.CLOSE_REVENUE);
			// Right Axis
			cy.findByText(lc.METRIC_LABEL.IMPRESSIONS);
		});
	});

	it("chart has tooltip with value formatted as currency", () => {
		cy.visit("/dashboard/reporting");

		// Spy on performance endpoint
		cy.intercept("GET", "**/manage/metrics/performance*", {
			fixture: "reporting/hourlyPerformanceData.json",
		});

		// Hover over chart
		cy.get(".recharts-surface").trigger("mouseover", 100, 100);
		cy.findByRole("dialog").within(() => {
			cy.findByText("1am");
			cy.findByText(lc.METRIC_LABEL.GROSS_REVENUE);
			cy.findByText("$1,000.46", {
				exact: true, // make sure there's no trailing digits
			});
			cy.findByText(lc.METRIC_LABEL.IMPRESSIONS);
			cy.findByText("1,500", {
				exact: true, // make sure there's no "$" symbol
			});
		});
	});

	it("charts show correct color metric for company", () => {
		const companyName = "Company Color Chart";

		const primaryColor = DEFAULT_COMPANY_REQUEST_BODY.branding.config.primaryColor;

		const color = Object.values(PRIMARY_COLORS).find((p) => p.id === primaryColor);

		const expectedSecundaryColor = convertHexToRGB(color.secondary.id);

		createOrUpdateCompany({ companyName }).then(({ body: { id: companyId } }) => {
			cy.visit(`/dashboard/reporting/?companyId=${companyId}`);

			// Spy on performance endpoint
			cy.intercept("GET", "**/manage/metrics/performanc*", {
				fixture: "reporting/hourlyPerformanceData.json",
			});

			cy.findByTestId(chartContainerTestId).within(() => {
				// We are only texting Right Axis is the secondary color, because the left Axis is the primary color (mui theme)
				cy.findByText(lc.METRIC_LABEL.IMPRESSIONS).should(($labels) => {
					expect($labels).to.have.css("color", expectedSecundaryColor);
				});
			});
		});
	});

	it("Change metric type from dropdown changes data on the graph", () => {
		cy.visit("/dashboard/reporting");

		// Spy on performance endpoint
		cy.intercept("GET", "**/manage/metrics/performance*", {
			fixture: "reporting/hourlyPerformanceData.json",
		});
		// change the left metric type
		cy.findByRole("button", { name: lc.METRIC_LABEL.GROSS_REVENUE }).click();
		cy.findByRole("option", { name: lc.METRIC_LABEL.QUARTILE_0 }).click();

		// ensure left metric is changed on the chart, check the tooltip to validate this
		cy.get(".recharts-surface").trigger("mouseover", 100, 100);
		cy.findByRole("dialog").within(() => {
			cy.findByText("1am");
			cy.findByText(lc.METRIC_LABEL.QUARTILE_0);
			cy.findByText("100%", {
				exact: true, // make sure there's no trailing digits
			});
			cy.findByText(lc.METRIC_LABEL.IMPRESSIONS);
			cy.findByText("1,500", {
				exact: true, // make sure there's no "$" symbol
			});
		});

		// change the right metric type
		cy.findByRole("button", { name: lc.METRIC_LABEL.IMPRESSIONS }).click();
		cy.findByRole("option", { name: lc.METRIC_LABEL.QUARTILE_100 }).click();

		// ensure right metric is changed on the chart, check the tooltip to validate this
		cy.get(".recharts-surface").trigger("mouseover", 100, 100);
		cy.findByRole("dialog").within(() => {
			cy.findByText("1am");
			cy.findByText(lc.METRIC_LABEL.QUARTILE_0);
			cy.findByText("100%", {
				exact: true, // make sure there's no trailing digits
			});
			cy.findByText(lc.METRIC_LABEL.QUARTILE_100);
			cy.findByText("33%", {
				exact: true, // make sure there's no "$" symbol
			});
		});
	});

	it("Close Rate tooltip should be percentage type on the graph", () => {
		cy.visit("/dashboard/reporting");

		// Setting date range today so that the graph is visible
		cy.clickElement(locators.dateRange);
		cy.clickElement(locators.dateRangeButtonToday);
		// Click on run report button
		cy.clickElement(locators.runReportButton);
		// Switch to RTB
		cy.clickElement(locators.rtbTab);

		// Spy on performance endpoint
		cy.intercept("GET", "**/manage/metrics/performance*", {
			fixture: "reporting/hourlyPerformanceData.json",
		});
		// change the left metric type
		cy.findByRole("button", { name: lc.METRIC_LABEL.CLOSE_REVENUE }).click();
		cy.findByRole("option", { name: lc.METRIC_LABEL.CLOSE_RATE }).click();

		// ensure left metric is changed on the chart, check the tooltip to validate this
		cy.get(".recharts-surface").trigger("mouseover", 300, 100);
		cy.findByRole("dialog").within(() => {
			cy.findByText("5am");
			cy.findByText(lc.METRIC_LABEL.CLOSE_RATE);
			cy.findByText("%", {
				exact: false,
			});
			//cy.findByText(lc.METRIC_LABEL.IMPRESSIONS);
			/*cy.findByText("0", {
				exact: true,
			});*/
		});
	});
});
