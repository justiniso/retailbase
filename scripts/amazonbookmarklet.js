// Minified
javascript:void function(){window.prompt("",JSON.stringify({title:jQuery("#productTitle").text(),brand:"Amazon",description:jQuery("#productDescription > p").text().trim(),price:parseFloat(jQuery("#priceblock_ourprice").text().replace("$","")),thumbnail_url:jQuery("img#landingImage").attr("src"),slug:document.URL.split("/")[3],link_url:"",tags:""},null,4))}();

// Original
javascript:void(function() { window.prompt("", JSON.stringify({
    "title": jQuery("#productTitle").text(),
    "brand": "Amazon",
    "description": jQuery("#productDescription > p").text().trim(),
    "price": parseFloat(jQuery('#priceblock_ourprice').text().replace("$", "")),
    "thumbnail_url": jQuery('img#landingImage').attr('src'),
    "slug": document.URL.split('/')[3],
    "link_url": "",
    "tags": ""
}, null, 4)) }());
