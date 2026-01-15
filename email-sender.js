
(function() {
    emailjs.init("soiyR8V0tm9I-at2-");
})();

function sendAuditDatatoEmail(dataObject) {
    // 1. Log the data clearly to the console
    console.group("📧 MOCK EMAIL SENDING");
    console.log("Received Data Object:", dataObject);


    // Check how the params would look for EmailJS
    const templateParams = {
        company_name: dataObject["Company Name"],
        reply_to: dataObject["Work Email"],
        website_url: dataObject["Website URL"],
        goal: dataObject["Primary Goal"]
    };
    console.log("Formatted Template Params:", templateParams);
    console.groupEnd();

    const serviceID = 'service_lg9uqt9'
    const templateID= 'template_5w8l5jb'

    // 2. Return a Promise with a delay to simulate a real network request.
    // This ensures your "await" in the main file works and you see the spinner.
    return emailjs.send(serviceID, templateID, templateParams)
        .then(function(response){
            console.log('SUCCESS!', response.status, response.text);
            return response;
        }, function(error){
            console.log('Failed....', error);
            throw error;
        });
}