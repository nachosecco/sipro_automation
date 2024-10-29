import { DEFAULT_PLACEMENT_BODY } from "../../../fixtures/defaultSupplySideCreationData";
import { globalContent } from "../../../locators/globalLocators";
import { localeContent } from "../../../locators/routerLocator";
import { createOrUpdatePlacement } from "../../../support/supplyCommands";
import getPrimaryCompanyId from "../../../utils/getPrimaryCompany";
import { INVENTORY_ROUTERS_API } from "../../../utils/serviceResources";

describe("Routers Smoke Test", () => {
	const currentTime = new Date().getTime();

	const routerName = "Automation Router Smoke";

	const routerNameSmoke = `${routerName}[${currentTime}]`;

	beforeEach(() => {
		cy.loginProgrammatically().then(() => {
			const pathDeleteResource = (resource) => {
				return INVENTORY_ROUTERS_API.ROUTER.getOne({ id: resource.id });
			};
			const companyId = getPrimaryCompanyId();
			const indexPathResources = INVENTORY_ROUTERS_API.ROUTER.getIndex({ companyId });

			const filterResourceToDelete = (resource) => resource.name.startsWith(routerName);
			cy.cleanResources({ indexPathResources, pathDeleteResource, filterResourceToDelete });
		});
	});

	it("Smoke tests a Router", () => {
		//Preparation
		cy.intercept("GET", "**/routers*").as("routers");

		cy.intercept("POST", "**/routers*").as("routersPost");

		cy.intercept("PUT", "**/routers/*").as("routersPut");

		cy.intercept("DELETE", "**/routers/*").as("routersDelete");

		const TAG_EXAMPLE = "https://example";

		const routerNameSmokeEdit = `${routerNameSmoke} Edited`;

		//Navigate to routers index
		cy.visit("dashboard/routers");
		cy.findByRole("heading", { name: localeContent.ROUTERS }).should("exist");

		cy.wait("@routers").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		//Add a Router
		cy.findByRole("link", { name: localeContent.ADD_ROUTER }).click();

		cy.wait("@routers").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		cy.findByRole("heading", { name: localeContent.ADD_ROUTER }).should("exist");

		cy.findByLabelText(localeContent.ROUTER_NAME).type(routerNameSmoke);

		cy.findByLabelText(localeContent.DEMAND_TYPE).click();

		cy.findByRole("option", { name: localeContent.DEMAND_SOURCE_TYPE_THIRD_PARTY }).click();

		cy.findByLabelText(localeContent.DEMAND_SOURCE).type(TAG_EXAMPLE);
		cy.findByLabelText(localeContent.ALLOCATION).type(100);

		cy.findByRole("button", { name: globalContent.SAVE }).click();

		cy.wait("@routersPost", { timeout: 10000 }).then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 201);
		});

		cy.contains(globalContent.SUCCESSFULLY_CREATED_SUFFIX);

		//Navigate to Router Index to find the new router
		cy.visit("dashboard/routers");

		cy.wait("@routers").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		cy.search(routerNameSmoke);

		//Navigate to Router Edit
		cy.clickDataGridEditMenuItem();

		cy.wait("@routers").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		cy.findByLabelText(localeContent.ROUTER).should("exist").should("be.disabled");

		cy.findByLabelText(localeContent.ROUTER_NAME).should("have.value", routerNameSmoke);

		cy.findByLabelText(localeContent.DEMAND_SOURCE).should("have.value", TAG_EXAMPLE);

		cy.findByLabelText(localeContent.ALLOCATION).should("have.value", 100);

		cy.findByLabelText(localeContent.ROUTER_NAME).clear().type(routerNameSmokeEdit);

		cy.findByRole("button", { name: globalContent.SAVE }).click();

		cy.wait("@routersPut").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		cy.contains(globalContent.SUCCESSFULLY_UPDATED_SUFFIX);

		//Navigate to Router Index

		cy.visit("dashboard/routers");

		cy.wait("@routers").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		cy.search(routerNameSmokeEdit);

		//Navigate to Router Edit to check if have the edited value

		cy.clickDataGridEditMenuItem();

		cy.wait("@routers").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		cy.findByLabelText(localeContent.ROUTER_NAME).should("have.value", routerNameSmokeEdit);

		//Navigate to Router Index to do a Delete
		cy.visit("dashboard/routers");

		cy.wait("@routers").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		cy.search(routerNameSmokeEdit);

		//Deleting the created router
		cy.clickDataGridDeleteMenuItem();

		cy.findByRole("button", { name: globalContent.DELETE }).click();

		cy.wait("@routersDelete").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 204);
		});

		cy.contains(globalContent.SUCCESSFULLY_DELETED_SUFFIX);
	});
});

//Test case : Create a router with valid placement for type app and then edit and delete the router .
describe("Create a Router with valid placement and then edit and delete the router", () => {
	const currentTime = new Date().getTime();

	const routerNamePrefix = "(UI) Router App valid placement";
	const routerName = `${routerNamePrefix}[${currentTime}]`;
	const publisername = "(UI) Router Test supply - Publisher ";
	const sitename = "(UI) Router Test supply - site ";
	const placementname = "(UI) Router Test supply - Placement ";

	beforeEach(() => {
		cy.loginProgrammatically().then(() => {
			const pathDeleteResource = (resource) => {
				return INVENTORY_ROUTERS_API.ROUTER.getOne({ id: resource.id });
			};
			const companyId = getPrimaryCompanyId();
			const indexPathResources = INVENTORY_ROUTERS_API.ROUTER.getIndex({ companyId });

			const filterResourceToDelete = (resource) => resource.name.startsWith(routerNamePrefix);
			cy.cleanResources({ indexPathResources, pathDeleteResource, filterResourceToDelete });
		});
	});

	it("Create a router with valid Placement", () => {
		//create or update placement
		createOrUpdatePlacement({
			publisherName: publisername,
			siteName: sitename,
			placementName: placementname,
			placementBody: { ...DEFAULT_PLACEMENT_BODY },
		}).then((response) => {
			const placementResponse = response.body;

			//Preparation
			cy.intercept("GET", "**/routers*").as("routers");

			cy.intercept("POST", "**/routers*").as("routersPost");

			cy.intercept("PUT", "**/routers/*").as("routersPut");

			cy.intercept("DELETE", "**/routers/*").as("routersDelete");

			cy.intercept("GET", "**/placements*").as("placements");

			const routerNameEdit = `${routerName} Edited`;

			//Navigate to routers index
			cy.visit("dashboard/routers");
			cy.findByRole("heading", { name: localeContent.ROUTERS }).should("exist");

			cy.wait("@routers").then(({ response }) => {
				cy.wrap(response.statusCode).should("equal", 200);
			});

			//Add a Router
			cy.findByRole("link", { name: localeContent.ADD_ROUTER }).click();

			cy.wait("@routers").then(({ response }) => {
				cy.wrap(response.statusCode).should("equal", 200);
			});

			cy.findByRole("heading", { name: localeContent.ADD_ROUTER }).should("exist");
			cy.wait("@placements").then(({ response }) => {
				cy.wrap(response.statusCode).should("equal", 200);
			});

			cy.findByLabelText(localeContent.ROUTER_NAME).type(routerName);

			cy.findByLabelText(localeContent.DEMAND_TYPE).click();

			cy.findByRole("option", { name: localeContent.DEMAND_SOURCE_TYPE_PLACEMENT }).click();
			cy.findByLabelText(localeContent.DEMAND_SOURCE).type(placementname);

			cy.findByRole("option", { id: "demandSources-0-placementId-option-0" }).click();
			cy.findByLabelText(localeContent.ALLOCATION).type(100);

			cy.findByRole("button", { name: globalContent.SAVE }).click();

			cy.wait("@routersPost", { timeout: 10000 }).then(({ response }) => {
				cy.wrap(response.statusCode).should("equal", 201);
			});

			cy.contains(globalContent.SUCCESSFULLY_CREATED_SUFFIX);

			//Navigate to Router Index to find the new router
			cy.visit("dashboard/routers");

			cy.wait("@routers").then(({ response }) => {
				cy.wrap(response.statusCode).should("equal", 200);
			});

			cy.search(routerName);

			//Navigate to Router Edit
			cy.clickDataGridEditMenuItem();

			cy.wait("@routers").then(({ response }) => {
				cy.wrap(response.statusCode).should("equal", 200);
			});

			cy.findByLabelText(localeContent.ROUTER).should("exist").should("be.disabled");

			cy.findByLabelText(localeContent.ROUTER_NAME).should("have.value", routerName);

			cy.findByLabelText(localeContent.DEMAND_SOURCE).should("have.value", placementResponse.name);

			cy.findByLabelText(localeContent.ALLOCATION).should("have.value", 100);

			cy.findByLabelText(localeContent.ROUTER_NAME).clear().type(routerNameEdit);

			cy.findByRole("button", { name: globalContent.SAVE }).click();

			cy.wait("@routersPut").then(({ response }) => {
				cy.wrap(response.statusCode).should("equal", 200);
			});

			cy.contains(globalContent.SUCCESSFULLY_UPDATED_SUFFIX);

			//Navigate to Router Index

			cy.visit("dashboard/routers");

			cy.wait("@routers").then(({ response }) => {
				cy.wrap(response.statusCode).should("equal", 200);
			});

			cy.search(routerNameEdit);

			//Navigate to Router Edit to check if have the edited value

			cy.clickDataGridEditMenuItem();

			cy.wait("@routers").then(({ response }) => {
				cy.wrap(response.statusCode).should("equal", 200);
			});

			cy.findByLabelText(localeContent.ROUTER_NAME).should("have.value", routerNameEdit);

			//Navigate to Router Index to do a Delete
			cy.visit("dashboard/routers");

			cy.wait("@routers").then(({ response }) => {
				cy.wrap(response.statusCode).should("equal", 200);
			});

			cy.search(routerNameEdit);

			//Deleting the created router
			cy.clickDataGridDeleteMenuItem();

			cy.findByRole("button", { name: globalContent.DELETE }).click();

			cy.wait("@routersDelete").then(({ response }) => {
				cy.wrap(response.statusCode).should("equal", 204);
			});

			cy.contains(globalContent.SUCCESSFULLY_DELETED_SUFFIX);
		});
	});
});

describe("Create a Router With an Invalid Placement and then edit and delete the router", () => {
	const currentTime = new Date().getTime();

	const routerNamePrefix = "Automation Router Invalid Placement";
	const routerNameInvalid = `${routerNamePrefix}[${currentTime}]`;

	beforeEach(() => {
		cy.loginProgrammatically().then(() => {
			const pathDeleteResource = (resource) => {
				return INVENTORY_ROUTERS_API.ROUTER.getOne({ id: resource.id });
			};
			const companyId = getPrimaryCompanyId();
			const indexPathResources = INVENTORY_ROUTERS_API.ROUTER.getIndex({ companyId });

			const filterResourceToDelete = (resource) => resource.name.startsWith(routerNamePrefix);
			cy.cleanResources({ indexPathResources, pathDeleteResource, filterResourceToDelete });
		});
	});

	it("Create a Router with an Invalid Placement", () => {
		//Preparation
		cy.intercept("GET", "**/routers*").as("routers");

		cy.intercept("POST", "**/routers*").as("routersPost");

		cy.intercept("PUT", "**/routers/*").as("routersPut");

		cy.intercept("DELETE", "**/routers/*").as("routersDelete");

		cy.intercept("GET", "**/placements*").as("placements");

		//Creating a Placement, with a status disabled
		createOrUpdatePlacement({
			publisherName: "(UI) Publisher",
			siteName: "(UI)- Site",
			placementName: "(UI) Placement for Router Inactive",
			placementBody: { ...DEFAULT_PLACEMENT_BODY, status: "inactive" },
		}).then((response) => {
			const placementCreated = response.body;
			//Navigate to routers index
			cy.visit("dashboard/routers");
			cy.findByRole("heading", { name: localeContent.ROUTERS }).should("exist");

			cy.wait("@routers").then(({ response }) => {
				cy.wrap(response.statusCode).should("equal", 200);
			});

			//Add a Router
			cy.findByRole("link", { name: localeContent.ADD_ROUTER }).click();

			cy.wait("@routers").then(({ response }) => {
				cy.wrap(response.statusCode).should("equal", 200);
			});

			cy.findByRole("heading", { name: localeContent.ADD_ROUTER }).should("exist");

			cy.wait("@placements").then(({ response }) => {
				cy.wrap(response.statusCode).should("equal", 200);
			});

			cy.findByLabelText(localeContent.ROUTER_NAME).type(routerNameInvalid);

			cy.findByLabelText(localeContent.ALLOCATION).type(100);

			cy.findByLabelText(localeContent.DEMAND_SOURCE).type(placementCreated.name);

			cy.findAllByRole("option", { name: placementCreated.name }).first().click();

			cy.findByRole("button", { name: globalContent.SAVE }).click();

			cy.wait("@routersPost", { timeout: 5000 }).then(({ response }) => {
				cy.wrap(response.statusCode).should("equal", 400);
			});

			cy.contains(localeContent.WARNING_WITH_PLACEMENT_INNACTIVE);
		});
	});
});

describe("Create a Router for router type App with placement and 3rd party with 50 percent allocations", () => {
	//Test case : Create a router with 2 placements:
	//		1. A valid placement-50%
	//		2. A 3rd party-50%
	const currentTime = new Date().getTime();
	const routerNamePrefix = "(UI) Router App placement and 3rd party";
	const routerName = `${routerNamePrefix}[${currentTime}]`;
	const publisername = "(UI) Router Test supply - Publisher ";
	const sitename = "(UI) Router Test supply - site ";
	const placementname = "(UI) Router Test supply - Placement ";

	beforeEach(() => {
		cy.loginProgrammatically().then(() => {
			const pathDeleteResource = (resource) => {
				return INVENTORY_ROUTERS_API.ROUTER.getOne({ id: resource.id });
			};
			const companyId = getPrimaryCompanyId();
			const indexPathResources = INVENTORY_ROUTERS_API.ROUTER.getIndex({ companyId });

			const filterResourceToDelete = (resource) => resource.name.startsWith(routerNamePrefix);
			cy.cleanResources({ indexPathResources, pathDeleteResource, filterResourceToDelete });
		});
	});

	it("Create with placement and 3rd party with 50 percent allocations", () => {
		const Tag3rdParty = "https://cdndev.siprocalads.com/c6internaltestpage/test_vast_mp4.xml?";
		//create or update placement
		createOrUpdatePlacement({
			publisherName: publisername,
			siteName: sitename,
			placementName: placementname,
			placementBody: { ...DEFAULT_PLACEMENT_BODY },
		}).then((response) => console.log("response", response));
		//Preparation
		cy.intercept("GET", "**/routers*").as("routers");

		cy.intercept("POST", "**/routers*").as("routersPost");

		cy.intercept("PUT", "**/routers/*").as("routersPut");

		cy.intercept("DELETE", "**/routers/*").as("routersDelete");

		cy.intercept("GET", "**/placements*").as("placements");

		const routerNameEdit = `${routerName} Edited`;

		//Navigate to routers index
		cy.visit("dashboard/routers");
		cy.findByRole("heading", { name: localeContent.ROUTERS }).should("exist");

		cy.wait("@routers").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		//Add a Router
		cy.findByRole("link", { name: localeContent.ADD_ROUTER }).click();

		cy.wait("@routers").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		cy.findByRole("heading", { name: localeContent.ADD_ROUTER }).should("exist");
		cy.wait("@placements").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		cy.findByLabelText(localeContent.ROUTER_NAME).type(routerName);

		cy.findByLabelText(localeContent.DEMAND_TYPE).click();

		cy.findByRole("option", { name: localeContent.DEMAND_SOURCE_TYPE_PLACEMENT }).click();
		cy.findByLabelText(localeContent.DEMAND_SOURCE).type(placementname);

		cy.findByRole("option", { id: "demandSources-0-placementId-option-0" }).click();

		cy.findByLabelText(localeContent.ALLOCATION).type(50).blur();

		//Add another demand source

		cy.findByRole("button", { name: localeContent.ADD_DEMAND_SOURCE }).click();

		cy.findAllByLabelText(localeContent.DEMAND_TYPE).eq(1).click();

		cy.findByRole("option", { name: localeContent.DEMAND_SOURCE_TYPE_THIRD_PARTY }).click();

		cy.findAllByLabelText(localeContent.DEMAND_SOURCE).eq(1).type(Tag3rdParty);
		cy.findAllByLabelText(localeContent.ALLOCATION).eq(1).type(50);
		cy.findByRole("button", { name: globalContent.SAVE }).click();

		cy.wait("@routersPost").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 201);
		});

		cy.contains(globalContent.SUCCESSFULLY_CREATED_SUFFIX);

		//Navigate to Router Index to find the new router
		cy.visit("dashboard/routers");

		cy.wait("@routers").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		cy.search(routerName);

		//Navigate to Router Edit
		cy.clickDataGridEditMenuItem();

		cy.wait("@routers").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});
		//Add assert validations
		cy.findByLabelText(localeContent.ROUTER).should("exist").should("be.disabled");

		cy.findByLabelText(localeContent.ROUTER_NAME).should("have.value", routerName);

		cy.findAllByLabelText(localeContent.DEMAND_SOURCE).eq(0).should("have.value", placementname);

		cy.findAllByLabelText(localeContent.ALLOCATION).eq(0).should("have.value", 50);

		cy.findAllByLabelText(localeContent.DEMAND_SOURCE)
			.eq(1)
			.should("have.value", "https://cdndev.siprocalads.com/c6internaltestpage/test_vast_mp4.xml?");

		cy.findAllByLabelText(localeContent.ALLOCATION).eq(1).should("have.value", 50);

		cy.findByLabelText(localeContent.ROUTER_NAME).clear().type(routerNameEdit);

		cy.findByRole("button", { name: globalContent.SAVE }).click();

		cy.wait("@routersPut").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		cy.contains(globalContent.SUCCESSFULLY_UPDATED_SUFFIX);

		//Navigate to Router Index

		cy.visit("dashboard/routers");

		cy.wait("@routers").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		cy.search(routerNameEdit);

		//Navigate to Router Edit to check if have the edited value

		cy.clickDataGridEditMenuItem();

		cy.wait("@routers").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		cy.findByLabelText(localeContent.ROUTER_NAME).should("have.value", routerNameEdit);

		//Navigate to Router Index to do a Delete
		cy.visit("dashboard/routers");

		cy.wait("@routers").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		cy.search(routerNameEdit);

		//Deleting the created router
		cy.clickDataGridDeleteMenuItem();

		cy.findByRole("button", { name: globalContent.DELETE }).click();

		cy.wait("@routersDelete").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 204);
		});

		cy.contains(globalContent.SUCCESSFULLY_DELETED_SUFFIX);
	});
});
describe("Create a Router for router type WEB and then edit and delete the router", () => {
	//Test case : Create a router with web router type:
	const currentTime = new Date().getTime();
	const routerName = `(UI) Router App placement router type web [${currentTime}]`;
	const publisername = "(UI) Router Test supply - Publisher ";
	const sitename = "(UI) Router Test supply - site ";
	const placementname = "(UI) Router Test supply - Placement vast ";

	beforeEach(() => {
		cy.loginProgrammatically();
	});

	it("Create a Router for router type web", () => {
		//create or update placement
		createOrUpdatePlacement({
			publisherName: publisername,
			siteName: sitename,
			placementName: placementname,
			//create a instream vast tag placement
			placementBody: {
				...DEFAULT_PLACEMENT_BODY,
				type: "vast",
				enableVPAID: "true",
				enableC6AdManager: "true",
			},
		}).then((response) => console.log("response", response));
		//Preparation
		cy.intercept("GET", "**/routers*").as("routers");

		cy.intercept("POST", "**/routers*").as("routersPost");

		cy.intercept("PUT", "**/routers/*").as("routersPut");

		cy.intercept("DELETE", "**/routers/*").as("routersDelete");

		cy.intercept("GET", "**/placements*").as("placements");

		const routerNameEdit = `${routerName} Edited`;

		//Navigate to routers index
		cy.visit("dashboard/routers");
		cy.findByRole("heading", { name: localeContent.ROUTERS }).should("exist");

		cy.wait("@routers").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		//Add a Router
		cy.findByRole("link", { name: localeContent.ADD_ROUTER }).click();

		cy.wait("@routers").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		cy.findByRole("heading", { name: localeContent.ADD_ROUTER }).should("exist");
		cy.wait("@placements").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		cy.findByLabelText(localeContent.ROUTER_NAME).type(routerName);

		//Add Router Type WEB
		cy.findByLabelText(localeContent.ROUTER_TYPE).click();
		cy.findByRole("option", { name: localeContent.ROUTER_TYPE_WEB }).click();
		cy.findByLabelText(localeContent.DEMAND_TYPE).click();

		cy.findByRole("option", { name: localeContent.DEMAND_SOURCE_TYPE_PLACEMENT }).click();
		cy.findByLabelText(localeContent.DEMAND_SOURCE).type(placementname);

		cy.findByRole("option", { id: "demandSources-0-placementId-option-0" }).click();

		cy.findByLabelText(localeContent.ALLOCATION).type(100);

		cy.findByRole("button", { name: globalContent.SAVE }).click();

		cy.wait("@routersPost").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 201);
		});

		cy.contains(globalContent.SUCCESSFULLY_CREATED_SUFFIX);

		//Navigate to Router Index to find the new router
		cy.visit("dashboard/routers");

		cy.wait("@routers").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		cy.search(routerName);

		//Navigate to Router Edit
		cy.clickDataGridEditMenuItem();

		cy.wait("@routers").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});
		//Add assert validations
		cy.findByLabelText(localeContent.ROUTER).should("exist").should("be.disabled");

		cy.findByLabelText(localeContent.ROUTER_NAME).should("have.value", routerName);

		cy.findAllByLabelText(localeContent.DEMAND_SOURCE).eq(0).should("have.value", placementname);

		cy.findAllByLabelText(localeContent.ALLOCATION).eq(0).should("have.value", 100);

		cy.findByLabelText(localeContent.ROUTER_NAME).clear().type(routerNameEdit);

		cy.findByRole("button", { name: globalContent.SAVE }).click();

		cy.wait("@routersPut").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		cy.contains(globalContent.SUCCESSFULLY_UPDATED_SUFFIX);

		//Navigate to Router Index

		cy.visit("dashboard/routers");

		cy.wait("@routers").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		cy.search(routerNameEdit);

		//Navigate to Router Edit to check if have the edited value

		cy.clickDataGridEditMenuItem();

		cy.wait("@routers").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		cy.findByLabelText(localeContent.ROUTER_NAME).should("have.value", routerNameEdit);

		//Navigate to Router Index to do a Delete
		cy.visit("dashboard/routers");

		cy.wait("@routers").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 200);
		});

		cy.search(routerNameEdit);

		//Deleting the created router
		cy.clickDataGridDeleteMenuItem();

		cy.findByRole("button", { name: globalContent.DELETE }).click();

		cy.wait("@routersDelete").then(({ response }) => {
			cy.wrap(response.statusCode).should("equal", 204);
		});

		cy.contains(globalContent.SUCCESSFULLY_DELETED_SUFFIX);
	});
});
