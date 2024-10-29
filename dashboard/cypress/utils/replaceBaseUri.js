/**
 * Example usage:

	const oldUri = 'http://manage.siprocalads.com/path/to/resource';
	const newBaseUri = 'http://localhost:8082';
	const newUri = replaceBaseUri(oldUri, newBaseUri);

	console.log(newUri); // Outputs: http://localhost:8082/path/to/resource
 */
function replaceBaseUri(uri, newBaseUri) {
	// Define the regex to match the beginning part of the URI
	// NOTE: Regex was generated using ChatGPT
	const regex = /^(https?:\/\/[^/:]+(:\d+)?)/;

	// Replace the beginning part with the new base URI
	const newUri = uri.replace(regex, newBaseUri);

	return newUri;
}

export default replaceBaseUri;
