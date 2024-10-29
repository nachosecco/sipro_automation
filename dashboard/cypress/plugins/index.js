// The following code will allow us to select the environment where we want to
// run our test by providing --env variable on the command line execution
// for example "npx cypress run --env name=qa1"

/**
 * @type {Cypress.PluginConfig}
 */
const fs = require("fs-extra");
const path = require("path");

module.exports = (on, config) => {
	function processConfigName(on, config) {
		// We are using the file passed on --env, if not provided use int as default
		const file = config.env.name || "dev";
		const retries = parseInt(config.env.retries) || 0;
		return getConfigFile(file).then(function (file) {
			file.retries = retries;
			// Return file object
			return file;
		});
	}

	function getConfigFile(file) {
		const pathToConfigFile = path.resolve("cypress", "config", `${file}.json`);
		return fs.readJson(pathToConfigFile);
	}
	// Return the configuration file details
	return processConfigName(on, config);
};
