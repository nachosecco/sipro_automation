const componentToHex = (c) => {
	var hex = c.toString(16);
	return hex.length == 1 ? "0" + hex : hex;
};

export const convertRGBToHex = (r, g, b) => {
	return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
};

export const convertHexToRGB = (hex) => {
	var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
	const r = parseInt(result[1], 16);
	const g = parseInt(result[2], 16);
	const b = parseInt(result[3], 16);
	return `rgb(${r}, ${g}, ${b})`;
};
