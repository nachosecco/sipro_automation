import { audienceLocators, localeContent } from "../../../locators/audienceLocators";
import { globalContent } from "../../../locators/globalLocators";
import { getAudienceName } from "../../../utils/resourceNameUtil";
import { DASHBOARD_API } from "../../../utils/serviceResources";

const cleanup = (audienceName) => {
	const pathDeleteResource = (resource) => {
		return DASHBOARD_API.AUDIENCE.getOne({ id: resource.id });
	};
	const indexPathResources = DASHBOARD_API.ADVERTISER.getIndex();
	const filterResourceToDelete = (resource) => resource.name == audienceName;
	cy.cleanResources({ indexPathResources, pathDeleteResource, filterResourceToDelete });
};

describe("Audience creation test cases", () => {
	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Valid audience creation", () => {
		const audienceNames = getAudienceName("creation");
		cleanup(audienceNames.audienceName);

		// Visit audience index page
		cy.visit("/dashboard/audiences");

		// Verify that page title is audiences
		cy.findByRole("heading", { name: localeContent.INDEX_HEADING });

		// Assert presence of add audiencce button and click it
		cy.clickElement(audienceLocators.addAudienceButton);

		// Validate these elements are visible
		cy.verifyElementsExist(
			audienceLocators.audienceNameField,
			audienceLocators.descriptionField,
			audienceLocators.andOperator,
			audienceLocators.orOperator,
			audienceLocators.notOperator,
			audienceLocators.parenthesisOperator
		);

		// Fill the form and submit
		// TODO: Remove exception handler once https://beezag.jira.com/browse/CP-1897 is fixed
		Cypress.on("uncaught:exception", () => {
			return false;
		});
		cy.getByRole(audienceLocators.audienceNameField).type(audienceNames.audienceName);
		cy.getByRole(audienceLocators.descriptionField).type(audienceNames.audienceName);
		cy.getByPlaceholderText(audienceLocators.searchField).type("Accessories");
		cy.dragAndDropTargetSegment(audienceLocators.targetSegmentButton);

		cy.findByRole("button", { name: globalContent.SAVE }).click();

		// Validate pop message
		cy.validatePopupMessage(`${audienceNames.audienceName} ${globalContent.SUCCESSFULLY_CREATED_SUFFIX}`);
	});
});
