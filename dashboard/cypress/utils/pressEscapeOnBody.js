const pressEscapeOnBody = () => cy.get("body").type("{esc}");
export default pressEscapeOnBody;
