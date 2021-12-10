var text = "https://gatherer.wizards.com/Pages/Search/Default.aspx?name=+[";
function onRequest(info, tab) {
	var selection = info.selectionText;
	text = "https://gatherer.wizards.com/Pages/Search/Default.aspx?name=+[";
	text = text + selection.toString() + "]";
};

function onRequest2(info, tab) {
	var selection = info.selectionText;
	text = "https://scryfall.com/search?q=";
	text = text + selection.toString();

};


function onRequest3(info, tab) {
	var selection = info.selectionText;
	text = "https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=";
	text = text + selection.toString();

};

chrome.extension.onRequest.addListener(onRequest);
chrome.contextMenus.onClicked.addListener(function(tab) {
	chrome.tabs.create({url:text});

});
chrome.contextMenus.create({title:"MtG Card Fetch (Gatherer) '%s'",contexts: ["all"], "onclick": onRequest});
chrome.contextMenus.create({title:"MtG Card Fetch (Scryfall) '%s'",contexts: ["all"], "onclick": onRequest2});
chrome.contextMenus.create({title:"MtG Card Fetch (ID Lookup) '%s'",contexts: ["all"], "onclick": onRequest3});