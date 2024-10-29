import getPrimaryCompanyId from "./getPrimaryCompany";

export const DASHBOARD_API_PATH = `${Cypress.env("dashboardApi")}`;
export const appendPrefixDashboardApi = (path) => `${DASHBOARD_API_PATH}/v2/${path}`;
export const appendPrefixDashboardApiManage = (path) => appendPrefixDashboardApi(`manage/${path}`);

export const DASHBOARD_API = {
	COMPANY: {
		getIndex: () => appendPrefixDashboardApiManage("companies"),
		getOne: ({ id }) => appendPrefixDashboardApiManage(`companies/${id}`),
		getInit: () => appendPrefixDashboardApiManage(`companies/INIT`),
	},
	USER: {
		getIndex: () => appendPrefixDashboardApiManage("users"),
		getOne: ({ id }) => appendPrefixDashboardApiManage(`users/${id}`),
		getInit: () => appendPrefixDashboardApiManage(`users/INIT`),
	},
	USER_ROLES: {
		getIndex: () => appendPrefixDashboardApiManage("user-roles"),
		getOne: ({ id }) => appendPrefixDashboardApiManage(`user-roles/${id}`),
		getInit: () => appendPrefixDashboardApiManage(`user-roles/INIT`),
	},
	USER_SETTINGS: {
		get: () => appendPrefixDashboardApiManage("userSettings"),
	},
	ADVERTISER: {
		getIndex: () => appendPrefixDashboardApiManage("advtsrs"),
		getOne: ({ id }) => appendPrefixDashboardApiManage(`advtsrs/${id}`),
		getInit: () => appendPrefixDashboardApiManage(`advtsrs/INIT`),
	},
	INSERTION_ORDER: {
		getIndex: () => appendPrefixDashboardApiManage("insertion-orders"),
		getOne: ({ id }) => appendPrefixDashboardApiManage(`insertion-orders/${id}`),
		getInit: () => appendPrefixDashboardApiManage(`insertion-orders/INIT`),
	},
	CAMPAIGN: {
		getIndex: () => appendPrefixDashboardApiManage("campaigns"),
		getOne: ({ id }) => appendPrefixDashboardApiManage(`campaigns/${id}`),
		getInit: () => appendPrefixDashboardApiManage(`campaigns/INIT`),
	},
	MEDIA: {
		getIndex: () => appendPrefixDashboardApiManage("media"),
		getOne: ({ id }) => appendPrefixDashboardApiManage(`media/${id}`),
		getInit: () => appendPrefixDashboardApiManage(`media/INIT`),
		getAlignments: ({ id }) => appendPrefixDashboardApiManage(`media/${id}/alignments`),
	},
	PROGRAMMATIC_DEMAND: {
		getIndex: () => appendPrefixDashboardApiManage("programmatic-demand"),
		getOne: ({ id }) => appendPrefixDashboardApiManage(`programmatic-demand/${id}`),
		getInit: () => appendPrefixDashboardApiManage(`programmatic-demand/INIT`),
		getAlignments: ({ id }) => appendPrefixDashboardApiManage(`programmatic-demand/${id}/alignments`),
	},
	AUDIENCE: {
		getIndex: () => appendPrefixDashboardApiManage("audiences"),
		getOne: ({ id }) => appendPrefixDashboardApiManage(`audiences/${id}`),
		getInit: () => appendPrefixDashboardApiManage(`audiences/INIT`),
	},
	SEGMENTS: {
		getIndex: () => appendPrefixDashboardApiManage("segments"),
		getOne: ({ id }) => appendPrefixDashboardApiManage(`segments/${id}`),
		getInit: () => appendPrefixDashboardApiManage(`segments/INIT`),
	},
	RTB_BIDDER: {
		getIndex: () => appendPrefixDashboardApiManage("rtb-bidders"),
		getOne: ({ id }) => appendPrefixDashboardApiManage(`rtb-bidders/${id}`),
		getInit: () => appendPrefixDashboardApiManage(`rtb-bidders/INIT`),
	},
	RTB_BIDDER_SEAT: {
		getIndex: () => appendPrefixDashboardApiManage("rtb-bidders/bidder-seats"),
		getOne: ({ id }) => appendPrefixDashboardApiManage(`rtb-bidders/bidder-seats/${id}`),
	},
	SITE: {
		getIndex: () => appendPrefixDashboardApiManage("sites"),
		getOne: ({ id }) => appendPrefixDashboardApiManage(`sites/${id}`),
		getInit: () => appendPrefixDashboardApiManage(`sites/INIT`),
	},
	PUBLISHER: {
		getIndex: () => appendPrefixDashboardApiManage("publishers"),
		getOne: ({ id }) => appendPrefixDashboardApiManage(`publishers/${id}`),
		getInit: () => appendPrefixDashboardApiManage(`publishers/INIT`),
	},
	PLACEMENT: {
		getIndex: () => appendPrefixDashboardApiManage("placements"),
		getOne: ({ id }) => appendPrefixDashboardApiManage(`placements/${id}`),
		getInit: () => appendPrefixDashboardApiManage(`placements/INIT`),
		getAlignments: ({ id }) => appendPrefixDashboardApiManage(`placements/${id}/alignments`),
		getAllAlignments: () => appendPrefixDashboardApiManage("placements/alignments"),
	},
	RUN_REPORTS: {
		getIndex: () => appendPrefixDashboardApi("reports/run-reports"),
		getOne: ({ id }) => appendPrefixDashboardApi(`reports/run-reports/${id}`),
	},
	SCHEDULED_REPORTS: {
		getIndex: () =>
			appendPrefixDashboardApi(
				"reports/scheduled-reports?reportTypes%5B%5D=network&reportTypes%5B%5D=rtb&reportTypes%5B%5D=campaign"
			),
		getOne: ({ id }) => appendPrefixDashboardApi(`reports/scheduled-reports/${id}`),
	},
	NOTIFICATION: {
		getIndex: () => appendPrefixDashboardApiManage("notification"),
		getOne: ({ id }) => appendPrefixDashboardApiManage(`notification/${id}`),
		getInit: () => appendPrefixDashboardApiManage(`notification/INIT`),
	},
	DATA_DISTRIBUTION: {
		getIndex: () => appendPrefixDashboardApiManage("dataDistributions"),
		getOne: ({ id }) => appendPrefixDashboardApiManage(`dataDistributions/${id}`),
		getInit: () => appendPrefixDashboardApiManage(`dataDistributions/INIT`),
	},
};

const inventoryRouterPrefix = `${Cypress.env("inventoryRouter")}api/v1/model/company/`;

const appendPrefixInventoryRouter = (path) => `${inventoryRouterPrefix}${path}`;

export const INVENTORY_ROUTERS_API = {
	ROUTER: {
		getIndex: ({ companyId = getPrimaryCompanyId() }) => appendPrefixInventoryRouter(`${companyId}/routers`),
		getOne: ({ companyId = getPrimaryCompanyId(), id }) =>
			appendPrefixInventoryRouter(`${companyId}/routers/${id}`),
	},
};

export default {};
