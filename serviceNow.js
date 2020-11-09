var requestBody = "{\"short_description\":\"test\"}";

var client = new XMLHttpRequest();
client.open("post", "https://dukesandbox.service-now.com/api/now/table/incident");

client.setRequestHeader('Accept', 'application/json');
client.setRequestHeader('Content-Type', 'application/json');

//Eg. UserName="admin", Password="admin" for this code sample.
client.setRequestHeader('Authorization', 'Basic ' + btoa('api.bugBounty.oit' + ':' + 'L8v7*0r@Vr*qDUuC^FqjBA2oq7V34hzcGtBde$xm'));

client.onreadystatechange = function () {
	if (this.readyState == this.DONE) {
		document.getElementById("response").innerHTML = this.status + this.response;
	}
};
client.send(requestBody);