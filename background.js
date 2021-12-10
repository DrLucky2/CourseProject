var text = "https://gatherer.wizards.com/Pages/Search/Default.aspx?name=+[";
function onRequest(info, tab) {
	var selection = info.selectionText;
	text = "https://gatherer.wizards.com/Pages/Search/Default.aspx?name=+[";
	text = text + selection.toString() + "]";

};
chrome.extension.onRequest.addListener(onRequest);
chrome.contextMenus.onClicked.addListener(function(tab) {
	chrome.tabs.create({url:text});
});
chrome.contextMenus.create({title:"MtG Card Fetch '%s'",contexts: ["all"], "onclick": onRequest});