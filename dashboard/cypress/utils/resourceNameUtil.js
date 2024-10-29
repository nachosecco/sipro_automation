const AUTOMATION_PREFIX = "(UI)";

export const getDemandNames = (testResourceName) => {
	const advertiserName = `${AUTOMATION_PREFIX} ${testResourceName} - Advertiser`;
	const insertionOrderName = `${AUTOMATION_PREFIX} ${testResourceName} - IO`;
	const campaignName = `${AUTOMATION_PREFIX} ${testResourceName} - Campaign`;
	const mediaName = `${AUTOMATION_PREFIX} ${testResourceName} - Media`;

	return {
		advertiserName: advertiserName,
		insertionOrderName: insertionOrderName,
		campaignName: campaignName,
		mediaName: mediaName,
	};
};

export const getRoleName = (testResourceName) => `${AUTOMATION_PREFIX} ${testResourceName}`;

export const getUserNames = (testResourceName, email) => {
	const timeStamp = new Date().getTime();
	const emailValue = timeStamp + email;
	const firstName = `${AUTOMATION_PREFIX} ${testResourceName} - First name`;
	const lastName = "Test";
	const roleName = getRoleName(testResourceName);
	return {
		firstName: firstName,
		lastName: lastName,
		roleName: roleName,
		email: emailValue,
	};
};

export const getProgrammaticDemandNames = (testResourceName) => {
	const programmaticName = `${AUTOMATION_PREFIX} ${testResourceName} - Programmatic`;
	const bidderName = `${getBidderName(testResourceName)} - SiprocalDSPBidder`;

	return {
		programmaticName: programmaticName,
		bidderName: bidderName,
	};
};

export const getSupplyNames = (testResourceName) => {
	const publisherName = `${AUTOMATION_PREFIX} ${testResourceName} - Pub`;
	const siteName = `${AUTOMATION_PREFIX} ${testResourceName} - Site`;
	const placementName = `${AUTOMATION_PREFIX} ${testResourceName} - Placement`;

	return {
		publisherName: publisherName,
		siteName: siteName,
		placementName: placementName,
	};
};

export const getBidderName = (testResourceName) => `${AUTOMATION_PREFIX} ${testResourceName}`;

export const getAudienceName = (testResourceName) => {
	const audienceName = `${AUTOMATION_PREFIX} ${testResourceName}`;
	return {
		audienceName,
	};
};

// TODO: Use this for all simple cases
export const getTestResourceName = (testResourceName) => `${AUTOMATION_PREFIX} ${testResourceName}`;
