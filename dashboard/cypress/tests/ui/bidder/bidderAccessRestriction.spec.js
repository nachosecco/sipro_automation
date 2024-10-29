import DEFAULT_BIDDER_REQUEST_BODY from "../../../fixtures/defaultBidderRequestBody";
import { localeContent as programmaticLocaleContent } from "../../../locators/programmaticLocators";
import { globalContent } from "../../../locators/globalLocators";
import { createOrUpdateBidder } from "../../../support/bidderCommands";
import { createOrUpdateCompany } from "../../../support/companyCommands";
import { getBidderName, getProgrammaticDemandNames, getTestResourceName } from "../../../utils/resourceNameUtil";
import { DEFAULT_PROGRAMMATIC_REQUEST_BODY } from "../../../fixtures/defaultDemandSideCreationData";
import { createOrUpdateProgrammaticDemand } from "../../../support/demandCommands";

const PRIMARY_COMPANY_ID = 1;

describe("Bidder access restrictions", () => {
	beforeEach(() => {
		cy.loginGlobalUserProgrammatically();
	});

	it("bidder index should only include bidders created under the company-in-view", () => {
		// Create a secondary company to switch to
		const alphaCompanyName = getTestResourceName("Secondary Company");
		createOrUpdateCompany({ companyName: alphaCompanyName }).then(({ body: { id: secondaryCompanyId } }) => {
			// Create a bidder under the primary company
			const globalBidderName = getBidderName("Global Bidder");
			createOrUpdateBidder({ bidderName: globalBidderName });

			// Visit the index page for the primary company
			cy.visit("/dashboard/bidders");
			// Bidder should show
			cy.findByRole("cell", { name: globalBidderName }).should("exist");

			// Visit the index page for the secondary company
			cy.visit(`/dashboard/bidders?companyId=${secondaryCompanyId}`);
			// Global Bidder should not show
			cy.findByRole("cell", { name: globalBidderName }).should("not.exist");

			// Within the grid body, expect the no bidder rows because this is a new company and has no access to global bidders
			cy.findByText("No rows").should("exist");
		});
	});

	it("programmatic demand form should respect bidder restriction configurations when creating new demand", () => {
		// Create another two companies
		const alphaCompanyName = getTestResourceName("Bidder Access - Alpha");
		const betaCompanyName = getTestResourceName("Bidder Access - Beta");
		const allBidderName = getBidderName("Bidder Company Restriction - All");
		const whitelistBidderName = getBidderName("Bidder Company Restriction - Whitelist");
		const blacklistBidderName = getBidderName("Bidder Company Restriction - Blacklist");
		createOrUpdateCompany({ companyName: alphaCompanyName }).then(({ body: { id: alphaCompanyId } }) => {
			createOrUpdateCompany({ companyName: betaCompanyName }).then(({ body: { id: betaCompanyId } }) => {
				// Create 3 bidders, one with each with restriction
				// All
				createOrUpdateBidder({ bidderName: allBidderName });
				// Whitelist
				createOrUpdateBidder({
					bidderName: whitelistBidderName,
					bidderBody: {
						...DEFAULT_BIDDER_REQUEST_BODY,
						companyAccessRestrictionConfig: {
							accessRestriction: "whitelist",
							blacklist: [],
							whitelist: [PRIMARY_COMPANY_ID, alphaCompanyId],
						},
					},
				});
				// Blacklist
				createOrUpdateBidder({
					bidderName: blacklistBidderName,
					bidderBody: {
						...DEFAULT_BIDDER_REQUEST_BODY,
						companyAccessRestrictionConfig: {
							accessRestriction: "blacklist",
							blacklist: [alphaCompanyId],
							whitelist: [],
						},
					},
				});

				/**
				 * Visit create Programatic Demand form for primary company to verify:
				 *     - All 3 created bidders are available
				 */
				cy.visit("/dashboard/programmatic-demand/INIT");
				cy.findByRole("list", { name: "available bidders" }).within(() => {
					cy.findByRole("listitem", { name: allBidderName }).should("exist");
					cy.findByRole("listitem", { name: whitelistBidderName }).should("exist");
					cy.findByRole("listitem", { name: blacklistBidderName }).should("exist");
				});

				/**
				 * Visit create Programatic Demand form for Alpha company to verify:
				 *     - Blacklist bidder is not there (it blacklisted Alpha)
				 *     - Whitelist bidder is there (it whitelisted Alpha)
				 *     - All access bidder is there
				 */
				cy.visit(`/dashboard/programmatic-demand/INIT?companyId=${alphaCompanyId}`);
				cy.findByRole("list", { name: "available bidders" }).within(() => {
					cy.findByRole("listitem", { name: allBidderName }).should("exist");
					cy.findByRole("listitem", { name: whitelistBidderName }).should("exist");
					cy.findByRole("listitem", { name: blacklistBidderName }).should("not.exist");
				});

				/**
				 * Visit create Programatic Demand form for Beta company to verify:
				 *     - Blacklist bidder is there (it blacklisted Alpha)
				 *     - Whitelist bidder is not there (it did not whitelist Beta)
				 *     - All access bidder is there
				 */
				cy.visit(`/dashboard/programmatic-demand/INIT?companyId=${betaCompanyId}`);
				cy.findByRole("list", { name: "available bidders" }).within(() => {
					cy.findByRole("listitem", { name: allBidderName }).should("exist");
					cy.findByRole("listitem", { name: whitelistBidderName }).should("not.exist");
					cy.findByRole("listitem", { name: blacklistBidderName }).should("exist");
				});
			});
		});
	});

	it("user should not be able to save a new programmatic demand with a bidder that the user no longer has access to", () => {
		// Create another company
		const secondaryCompanyName = getTestResourceName("Bidder Company Restriction Stale UI Option");
		// Create a second bidder
		const bidderName = getBidderName("Bidder Access Stale UI Option");
		createOrUpdateCompany({ companyName: secondaryCompanyName }).then(({ body: { id: secondaryCompanyId } }) => {
			// Create a bidder that grants access to all companies
			createOrUpdateBidder({ bidderName });

			cy.visit(`/dashboard/programmatic-demand/INIT?companyId=${secondaryCompanyId}`);
			// Fill out required name field
			cy.findByLabelText(programmaticLocaleContent.FIELDS.NAME.LABEL).type("Bidder Company Restriction");
			// Select the all access bidder
			cy.findByRole("listitem", { name: bidderName }).within(() => {
				cy.findByRole("button", { name: programmaticLocaleContent.FIELDS.BIDDER_CONFIG.ADD_BIDDER }).click();
			});

			// Programmatically change the access of the bidder to blacklist the secondary company
			createOrUpdateBidder({
				bidderName,
				bidderBody: {
					...DEFAULT_BIDDER_REQUEST_BODY,
					companyAccessRestrictionConfig: {
						accessRestriction: "blacklist",
						blacklist: [secondaryCompanyId],
						whitelist: [],
					},
				},
			});

			cy.intercept("POST", "**/manage/programmatic-demand").as("createProgrammatic");

			// Save the form
			cy.findByRole("button", { name: globalContent.SAVE }).click();

			// POST should fail with 400
			cy.wait("@createProgrammatic").its("response.statusCode").should("eq", 400);

			// Error message should be rendered
			cy.contains(programmaticLocaleContent.ERROR_MESSAGE.POST_WITH_UNALLOWED_BIDDERS).should("exist");
		});
	});

	it("when access is removed from a bidder and user loads edit programmatic form that includes that bidder, should display an error message and prevent saving form", () => {
		// Create another company
		const testName = "Bidder Access Existing Unallowed";
		const programmaticDemandResourceNames = getProgrammaticDemandNames(testName);
		const secondaryCompanyName = getTestResourceName(testName);
		const bidderName = programmaticDemandResourceNames.bidderName;
		const programmaticName = programmaticDemandResourceNames.programmaticName;
		createOrUpdateCompany({ companyName: secondaryCompanyName }).then(({ body: { id: secondaryCompanyId } }) => {
			// Programmatically create a bidder that grants access to all companies
			createOrUpdateBidder({ bidderName }).then(({ body: { id: bidderId } }) => {
				// Programmatically create Programmatic Demand using the created bidder
				createOrUpdateProgrammaticDemand({
					programmaticName,
					bidderName,
					programmaticBody: {
						...DEFAULT_PROGRAMMATIC_REQUEST_BODY,
						programmaticBidderConfigs: [
							{
								rtbBidderId: bidderId,
								rtbBidderSeats: [],
							},
						],
					},
					headerExtensions: {
						"X-COMPANY-OVERRIDE": secondaryCompanyId,
					},
				}).then(({ body: { id: programmaticId } }) => {
					// Programmatically change the access of the bidder to blacklist the secondary company
					createOrUpdateBidder({
						bidderName,
						bidderBody: {
							...DEFAULT_BIDDER_REQUEST_BODY,
							companyAccessRestrictionConfig: {
								accessRestriction: "blacklist",
								blacklist: [secondaryCompanyId],
								whitelist: [],
							},
						},
					});

					// Visit the edit programatic form
					cy.visit(`/dashboard/programmatic-demand/${programmaticId}?companyId=${secondaryCompanyId}`);

					// Try to set status to active
					cy.findByLabelText(globalContent.STATUS_OPTION_LABEL.ACTIVE).click();

					cy.intercept("PUT", "**/manage/programmatic-demand/*").as("updateProgrammatic");

					// Save the form
					cy.findByRole("button", { name: globalContent.SAVE }).click();

					// PUT should fail with 400
					cy.wait("@updateProgrammatic").its("response.statusCode").should("eq", 400);

					// Error message should be rendered
					cy.contains(
						programmaticLocaleContent.ERROR_MESSAGE.ACTIVATE_EXISTING_WITH_UNALLOWED_BIDDERS
					).should("exist");
				});
			});
		});
	});
});
