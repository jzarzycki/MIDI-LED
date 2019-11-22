var express = require("express");
var app = express();
var bodyParser = require("body-parser");
var net = require('net');

app.use(express.static("public"));
app.use(bodyParser.urlencoded({extended: true}));
app.set("view engine", "ejs");

var drums = {
    "snare": {
        "flash": 40
    },
    "kick": {
        "wave-mid": 60
    },
    "hi-hat-closed": {
        "flash": 12
    },
    "crash": {
        "flash": 70,
    },
    "ride": {
        "flash": 6,
    },
};

var colors = [
    "#ffffff",
    "#ff0000",
    "#00ff00",
    "#0000ff",
    "#ffff00",
    "#00ffff",
    "#ff00ff"
];

var triggers = {
    "hi-hat-closed": "Closed Hi-Hat",
    "hi-hat-open": "Open Hi-Hat",
    "hi-hat-close": "Hi-Hat Pedal",
    "crash": "Crash",
    "ride": "Ride",
    "snare": "Snare",
    "kick": "Kick",
    "tom1": "Tom 1",
    "tom2": "Tom 2",
    "tom3": "Tom 3",
};

var animations = {
    "flash": "Flash",
    "bright-wave": "Brightness Wave",
    "wave": "Color Wave",
    "instant": "Instant Color",
};

function sendWithSocket(obj){
    var client = new net.Socket();
    client.connect(65432, '127.0.1.1', function() {
        client.write(JSON.stringify(obj));
    });
    client.on('data', function(data) {
        console.log('Received: ' + data);
        client.destroy();
    });
}

// delete drums[][] to delete key
app.post("/post", function(req, res){
    console.log(req.body);
    if (drums[req.body.name] == undefined) {
        drums[req.body.name] = {};
    }
    drums[req.body.name][req.body.animation] = req.body.option;
    res.redirect('/');
    
    sendWithSocket({[req.body.name]: {[req.body.animation]: req.body.option}})
});

function isEmpty(obj) {
    return Object.entries(obj).length === 0;
}

app.post("/delete", function(req, res){
    let trigger = req.query.trigger;
    let animation = req.query.animation;
    let obj = {[trigger]: {[animation]: null}};
    delete drums[trigger][animation]
    if (isEmpty(drums[trigger])) {
        delete drums[trigger]
        obj[trigger] = null;
    }
    res.redirect('/');
    console.log(obj);
    sendWithSocket(obj);
});

app.get("*", function(req, res){
    res.render("home", {drums: drums, colors: colors, triggers: triggers, animations: animations});
});

app.listen(13579, function(){
    console.log("Server started on port: 13579");
})
