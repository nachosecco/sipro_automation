import tracker, { localeContent } from "../../../locators/trackerLocators.js";
import appendRequired from "../../../utils/appendRequired.js";
import getToken from "../../../utils/getToken.js";
import macroLocators from "../../../locators/macroLocators";
const global = require("../../../locators/globalLocators.json");

const exampleName = "Automation Tracker";
const timeStamp = new Date().getTime();

describe("Tracker Form", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	afterEach(() => {
		cy.deleteTargetEntity(getToken(), `${exampleName} ${timeStamp}`, "tracker");
	});

	it("Tracker add DNT macro", () => {
		// Visit create tracker page
		cy.visit("/dashboard/trackers/INIT");

		// Add required field information
		cy.findByLabelText(appendRequired(localeContent.FIELDS.TRACKER_NAME.LABEL)).type(`${exampleName} ${timeStamp}`);
		cy.findByLabelText(appendRequired(localeContent.FIELDS.TRACKER_LABEL.LABEL)).type("Example tracker label");

		// Type a valid uri to start the tag
		const baseTrackerUrl = `www.automation-tracker-${timeStamp}.com?dnt=`;
		cy.findByLabelText(appendRequired(localeContent.FIELDS.TRACKER_URL.LABEL)).type(baseTrackerUrl);

		// Select DNT macro
		//cy.findByRole("button", { name: macroLocators.ADD_MACRO_LABEL }).click();
		//cy.findByRole("menuitem", { name: macroLocators.MACRO_OPTIONS.DNT.label }).click();
		cy.get(".MuiAutocomplete-root").find("input").type(macroLocators.MACRO_OPTIONS.DNT.label);
		cy.get(".MuiAutocomplete-option").click();

		// Submit form
		cy.clickElement(global.saveButton);

		// Expect success message
		cy.validatePopupMessage(`${exampleName} ${timeStamp} was successfully created`);

		// Validate DNT macro value
		cy.findByLabelText(appendRequired(localeContent.FIELDS.TRACKER_URL.LABEL)).contains(
			macroLocators.MACRO_OPTIONS.DNT.macro
		);
	});

	it("should disable and read-only media tracker if event is changed from impressions to opportunity", () => {
		// Visit create tracker page
		cy.visit("/dashboard/trackers/INIT");
		// Enable Media Tracker
		cy.clickElement(tracker.mediaTrackerCheckbox);
		// Enable Default Media Tracker
		cy.clickElement(tracker.defaultMediaTrackerCheckbox);
		// Select Opportunity as Event
		cy.clickElement(tracker.trackerEventDropdown);
		cy.clickElement(tracker.opportunityMenuItem);
		// Media Tracker should be disabled and unchecked
		cy.verifyElementsExist(tracker.mediaTrackerCheckbox).should("be.disabled");
		cy.verifyElementsExist(tracker.mediaTrackerCheckbox).should("not.be.checked");
	});

	it("Tracker URL field should include all supported macros", () => {
		// We don't allow users to add trackers with the same URL, Event, and Type, so we need to use a timestamp in the url
		const baseTrackerUrl = `www.automation-tracker-${timeStamp}.com?`;
		// Visit create tracker page
		cy.visit("/dashboard/trackers/INIT");

		// Add required field information
		cy.findByLabelText(appendRequired(localeContent.FIELDS.TRACKER_NAME.LABEL)).type(`${exampleName} ${timeStamp}`);
		cy.findByLabelText(appendRequired(localeContent.FIELDS.TRACKER_LABEL.LABEL)).type("Example tracker label");

		// Type a valid uri to start the tag
		cy.findByLabelText(appendRequired(localeContent.FIELDS.TRACKER_URL.LABEL)).type(baseTrackerUrl);

		// Select all macros
		Object.entries(macroLocators.MACRO_OPTIONS).forEach(([, categoryConfig]) => {
			//cy.findByRole("button", { name: macroLocators.ADD_MACRO_LABEL }).click();
			//cy.findByRole("menuitem", { name: categoryConfig.label }).click();

			cy.get(".MuiAutocomplete-root").find("input").clear();
			cy.get(".MuiAutocomplete-root").find("input").type(categoryConfig.label);
			cy.get(".MuiAutocomplete-option").find(`*[macro='${categoryConfig.macro}']`).click();
		});

		// Join all the macros from each category together into a single string

		const allMacrosString = Object.entries(macroLocators.MACRO_OPTIONS)
			.reduce((agg, [, categoryConfig]) => {
				return [...agg, ...categoryConfig.macro];
			}, [])
			.join("");

		// Tracker URL should have all expected macro strings in it
		cy.findByLabelText(appendRequired(localeContent.FIELDS.TRACKER_URL.LABEL)).should(
			"have.value",
			`${baseTrackerUrl}${allMacrosString}`
		);

		// Submit form
		cy.clickElement(global.saveButton);

		// All macros should be valid so expect success message
		cy.validatePopupMessage(`${exampleName} ${timeStamp} was successfully created`);
	});

	it("submission of unsupported macros in the Tracker URL should show field validation message", () => {
		// Visit create tracker page
		cy.visit("/dashboard/trackers/INIT");

		// Add required field information
		cy.findByLabelText(appendRequired(localeContent.FIELDS.TRACKER_NAME.LABEL)).type(`${exampleName} ${timeStamp}`);
		cy.findByLabelText(appendRequired(localeContent.FIELDS.TRACKER_LABEL.LABEL)).type("Example tracker label");

		// Type multiple invalid macros
		cy.findByLabelText(appendRequired(localeContent.FIELDS.TRACKER_URL.LABEL)).type(
			`www.invalid-automation-tracker-${timeStamp}.com?myCustomMacro=[my_custom_macro]&anotherCustom=[another_custom_macro]`
		);

		// Submit form
		cy.clickElement(global.saveButton);

		// Validation message should appear
		cy.findByText("Invalid Macros: [my_custom_macro], [another_custom_macro]");
	});
});
