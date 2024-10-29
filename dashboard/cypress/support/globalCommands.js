import { globalGridLocators } from "../locators/globalGridLocators";

const global = require("../locators/globalLocators.json");

const setLocalStorageItems = (res) => {
	window.localStorage.setItem("token", res.authorization);
	window.localStorage.setItem("userInfo", JSON.stringify({ username: res.username }));
	// Use 1 as default if response does not have a primary company id
	window.localStorage.setItem("primaryCompanyId", res.primaryCompanyId || 1);
	window.localStorage.setItem("isDemandClient", res.isDemandClient);
};

// This command will fetch the JWT and set it in the local storage of the browser
Cypress.Commands.add("loginProgrammatically", (config = {}) => {
	const { username = `${Cypress.env("uiUser")}`, password = `${Cypress.env("uiPassword")}` } = config;
	cy.request({
		url: Cypress.env("auth"),
		method: "POST",
		body: {
			username: username,
			password: password,
		},
	})
		.its("body")
		.then(setLocalStorageItems);
});

// Globaluser login

Cypress.Commands.add("loginGlobalUserProgrammatically", (config = {}) => {
	const { username = `${Cypress.env("globalUser")}`, password = `${Cypress.env("globalPassword")}` } = config;
	cy.request({
		url: Cypress.env("auth"),
		method: "POST",
		body: {
			username: username,
			password: password,
		},
	})
		.its("body")
		.then(setLocalStorageItems);
});

// This command takes web elemets as parameters and validates that they are visible
Cypress.Commands.add("verifyElementsExist", (...elements) => {
	for (var i = 0; i < elements.length; i++)
		cy.findByRole(elements[i].role, { name: elements[i].locator }).should("exist");
});

// This command takes web elemets as parameters and validates that they are not visible
Cypress.Commands.add("verifyElementsAreNotVisible", (...elements) => {
	for (var i = 0; i < elements.length; i++) cy.get(elements[i], { timeout: 10000 }).should("not.be.visible");
});

// This command will check if provided elements are not visible
Cypress.Commands.add("verifyElementsNotExist", (...elements) => {
	for (var i = 0; i < elements.length; i++)
		cy.findByRole(elements[i].role, { name: elements[i].locator }).should("not.exist");
});

// This command will verify that provided elements have Mui-required class
Cypress.Commands.add("verifyMandatoryFields", (...elements) => {
	for (var i = 0; i < elements.length; i++) cy.get(elements[i]).should("have.class", "Mui-required");
});

// This command will verify that provided parameters are checked (for checkboxes)
Cypress.Commands.add("verifyCheckedElements", (...elements) => {
	for (var i = 0; i < elements.length; i++)
		cy.findByRole(elements[i].role, { name: elements[i].locator }).should("be.checked");
});

// This command will uncheck provided checkboxes
Cypress.Commands.add("uncheckElements", (...elements) => {
	for (var i = 0; i < elements.length; i++) cy.findByRole(elements[i].role, { name: elements[i].locator }).uncheck();
});

// This function will get the curret timestamp in a specific format
export function currentTimestamp(date) {
	const day = date.getDate();
	const month = date.getMonth();
	const year = date.getFullYear();
	let hours = date.getHours();
	let minutes = date.getMinutes();
	const ampm = hours >= 12 ? "pm" : "am";
	hours = hours % 12;
	hours = hours ? hours : 12; // the hour '0' should be '12'
	minutes = minutes < 10 ? "0" + minutes : minutes;
	const strTime = `${day}/${month}/${year} ${hours}:${minutes} ${ampm.toUpperCase()}`;
	return strTime;
}

// The following funtions will use react testing library integration with Cypress to interact with web elements
Cypress.Commands.add("clickElement", (element) => {
	cy.findByRole(element.role, { name: element.locator }, { timeout: 10000 }).click({ timeout: 10000 });
});

Cypress.Commands.add("clickFirstElement", (element) => {
	cy.findAllByRole(element.role, { name: element.locator }, { timeout: 10000 }).eq(0).click();
});

Cypress.Commands.add("getByRole", (element) => {
	cy.findByRole(element.role, { name: element.locator }, { timeout: 10000 });
});

Cypress.Commands.add("getAllElementsByRole", (element) => {
	cy.findAllByRole(element.role, { name: element.locator }, { timeout: 10000 });
});

Cypress.Commands.add("getByPlaceholderText", (text) => {
	cy.findByPlaceholderText(text, { timeout: 10000 });
});

Cypress.Commands.add("getByLabelText", (text) => {
	cy.findByLabelText(text, { timeout: 10000 });
});

// This command will type a value into the search bar of an index page and order the results by name
Cypress.Commands.add("searchIndexPage", (value) => {
	cy.getByPlaceholderText(global.indexPageSearchBar).type(value);
});

Cypress.Commands.add("search", (value) => {
	cy.getByRole(globalGridLocators.searchBox).type(value);
	// Waiting to finish the debounce
	/* eslint-disable cypress/no-unnecessary-waiting */
	cy.wait(600);
});

// This command will wait for an input in the search box, then will click the action menu and the delete menu item
Cypress.Commands.add("clickDeleteMenuItem", () => {
	cy.getByRole(global.clearSearchButton).should("exist");
	cy.clickFirstElement(global.indexActionButton);
	cy.clickElement(global.indexDeleteMenuItem);
});
Cypress.Commands.add("clickDataGridDeleteMenuItem", () => {
	cy.getByRole(globalGridLocators.clearSearchButton).should("exist");
	cy.clickFirstElement(global.indexActionButton);
	cy.clickElement(global.indexDeleteMenuItem);
});

// This command will wait for an input in the search box, then will click the action menu and the edit menu item
Cypress.Commands.add("clickEditMenuItem", () => {
	cy.getByRole(global.clearSearchButton).should("exist");
	cy.clickFirstElement(global.indexActionButton);
	cy.clickElement(global.indexEditMenuItem);
});
Cypress.Commands.add("clickDataGridEditMenuItem", () => {
	cy.getByRole(globalGridLocators.clearSearchButton).should("exist");
	cy.clickFirstElement(global.indexActionButton);
	cy.clickElement(global.indexEditMenuItem);
});

// Commands bellow will work with radio elements inside a radio group
Cypress.Commands.add("verifyRadioByGroupExist", (group, radio) => {
	cy.getByRole(group).within(() => {
		cy.getByRole(radio).should("exist");
	});
});

Cypress.Commands.add("clickRadioByGroup", (group, radio) => {
	cy.getByRole(group).within(() => {
		cy.getByRole(radio).click();
	});
});

Cypress.Commands.add("validatePopupMessage", (text, options) => {
	cy.get(global.popUpMessage, options || {})
		.should("be.visible")
		.and("have.text", text);
});

Cypress.Commands.add("setDateByLabelText", (labelText, value) => {
	cy.findByLabelText(labelText).click();

	// Material-UI mobile date picker starts at the calendar view.
	// The first time we edit the date, we need to switch to the custom input view.
	// On subsequent edits of that date-picker instance,
	// it will reopen on the custom input view, so we don't need to navigate there.
	cy.get("body").then((body) => {
		if (body.find("[data-testid=PenIcon]").length > 0) {
			cy.get("[data-testid=PenIcon]").click();
		}
	});

	// Mui component textbox is unable to be found by label,
	// it shows up with an empty string as the name, which seems like a potential bug
	// with the mui implementation. It's the only visible textbox on the page at this point,
	//so we're leaving the empty string to be explicit in case another field is added by MUI
	cy.findByRole("textbox", { name: "" }).click().clear().type(value);

	cy.findByRole("dialog").within(() => {
		cy.findByRole("button", { name: "OK" }).click();
	});
});

Cypress.Commands.add("getDataGridData", (uniquePropertyValue, columnName, propertyName) => {
	return cy
		.contains("div.MuiDataGrid-columnHeaderTitle", columnName)
		.invoke("index")
		.then((index) => {
			cy.contains("div.MuiDataGrid-cellContent", uniquePropertyValue)
				.should("have.length", 1)
				.parent()
				.siblings("[data-field='" + propertyName + "']")
				.eq(index - 1)
				.invoke("text");
		});
});
