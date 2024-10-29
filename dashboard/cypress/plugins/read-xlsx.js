/// <reference types="cypress" />

// The following code will allow us to read data of xlsx file.

const fs = require("fs");
const XLSX = require("xlsx");

const read = ({ file, sheet, header }) => {
	const buf = fs.readFileSync(file);
	const workbook = XLSX.read(buf, { type: "buffer" });
	// For more information about sheet_to_json options, see https://www.npmjs.com/package/xlsx#json
	const rows = XLSX.utils.sheet_to_json(workbook.Sheets[sheet], { header });
	return rows;
};

module.exports = {
	read,
};
