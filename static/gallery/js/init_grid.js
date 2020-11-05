

window.onresize = doALoadOfStuff;

function doALoadOfStuff() {
    Macy({
    container: '#macy-container',
    trueOrder: true,
    waitForImages: false,
    margin: 18,
    columns: 3,
    breakAt: {
        1080: 2,
        720: 1
    }});
}
doALoadOfStuff()
doALoadOfStuff()
