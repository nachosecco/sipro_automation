export const locators = {
	newPasswordField: "New Password",
	confirmPasswordField: "Confirm Password",
	submitButton: { locator: "Submit", role: "button" },
};

export const localeContent = {
	invalidToken:
		"The authentication link provided is either invalid or has expired. Please enter your email address again to receive a new reset password email",
	upperCaseMissing: "Must contain atleast 1 uppercase character",
	minLength: "Must be minimum of 10 characters",
	specialCharMissing: "Must contain at least 1 of these special characters (@#$_^&+=!)",
	numberMissing: "Must contain atleast 1 numeric character",
	forgotPasswordLabel: "Forgot Password",
};
