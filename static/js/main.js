function post_request(target){
    let xmlhttp = getXmlHttp();
    xmlhttp.open('POST', target, true);
    xmlhttp.setRequestHeader("Content-Type", "application/json");
    xmlhttp.onload = () => {
        const data = JSON.parse(xmlhttp.responseText);
        if (!data.success){
            return;
        }
        return data
    }
    let tags = JSON.stringify({"target_case": case_name, "labels": labels, "inputs": inputs});
    xmlhttp.send(tags);
}

function create_card_class(link, name){
    let a = document.createElement("a");
    a.href = link;

    let card = document.createElement("div");
    card.className = "card";

    let card_body = document.createElement("div");
    card_body.className = "card-title";

    let title = document.createElement("h5");
    title.className = "card-title";
    title.innerText = name;

    let button = document.createElement("a")
    button.className = "btn btn-primary";
    button.href = link;
    button.innerText = "-->"

    title.setAttribute("onclick", "redirect(" + link + ");");

    let deck = document.getElementById("classes");
    deck.append(card);
    card.append(card_body);
    card_body.append(title);
    card_body.append(button)
}
