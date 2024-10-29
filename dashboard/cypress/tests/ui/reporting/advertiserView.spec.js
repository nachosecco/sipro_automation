import getToken from "../../../utils/getToken";
import advertiserData from "../../../fixtures/userAdvertiser";

const timeStamp = new Date().getTime();
const username = `${timeStamp}-advertiser-automation-user@test.com`;

describe("advertiser can login and view reporting", () => {
	beforeEach(() => {
		cy.loginGlobalUserProgrammatically();
		cy.createUserWithPermissions({
			userRoleName: advertiserData.userRoleName,
			username,
			permissionsToEnable: advertiserData.createUserPermissions,
		});
	});

	afterEach(() => {
		// Login with the Main test user to perform the new user delete operation.
		cy.loginProgrammatically().then(() => {
			// Adding it inside the callback because its an async call.
			// Delete User
			cy.deleteTargetEntity(getToken(), username, "user", "email");

			// Delete Company
			cy.deleteTargetEntity(getToken(), advertiserData.companyName, "company");
		});
	});

	it("Login with newly created test user and check if reporting is avaliable", () => {
		// Spy on performance endpoint
		cy.intercept("GET", "**/manage/metrics/performance*", {
			fixture: "reporting/hourlyPerformanceData.json",
		});
		// Login With New user
		cy.loginProgrammatically({
			username,
		});

		// visit reporting (and that is it, the user cannot do anything else)
		cy.visit("/dashboard/reporting");
	});
});
