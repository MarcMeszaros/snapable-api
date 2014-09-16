// document load
$(document).ready(function(){
    update_metrics();

    $('#metrics-refresh').click(function(){
        update_metrics();
    });
    $('#metrics-range form input[type="radio"]').change(function(){
        update_metrics();
    });
});

// simple wrapper to call all the metric update functions
function update_metrics() {
    metric_signups();
    metric_actives();
    past_events();
    photos_count();
    upcoming_events();
    past_events_photos();
    metrics();
}


// functions
function metric_signups() {
    var start = get_unix_start();
    $.getJSON('ajax/total_signups/'+start, function(json){
        $('#metric-signups .value').hide();
        $('#metric-signups .value').html(json.meta.total_count);
        $('#metric-signups .value').fadeIn();
    });
}

function metric_actives() {
    var start = get_unix_start();
    $.getJSON('ajax/total_actives/'+start, function(json){
        $('#metric-actives .value').hide();
        $('#metric-actives .value').html(json.meta.total_count);
        $('#metric-actives .value').fadeIn();
    });
}

function past_events() {
    var start = get_unix_start();
    $.getJSON('ajax/past_events/'+start, function(json){
        $('#metric-past-events-count .value').hide();
        $('#metric-past-events-count .value').html(json.meta.total_count);
        $('#metric-past-events-count .value').fadeIn();
    });
}

function photos_count() {
    var start = get_unix_start();
    $.getJSON('ajax/photos_count/'+start, function(json){
        $('#metric-photos-count .value').hide();
        $('#metric-photos-count .value').html(json.meta.total_count);
        $('#metric-photos-count .value').fadeIn();
    });
}

function upcoming_events() {
    var start = get_unix_start();
    $.getJSON('ajax/upcoming_events/'+start, function(json){
        $('#metric-upcoming-events .value').hide();
        $('#metric-upcoming-events .value').html(json.meta.total_count);
        $('#metric-upcoming-events .value').fadeIn();
    });
}

function past_events_photos() {
    var start = get_unix_start();
    $.getJSON('ajax/events_with_photo_count/1/'+start, function(json){
        $('#metric-past-events-photos .value').hide();
        $('#metric-past-events-photos .value').html(json.meta.total_count);
        $('#metric-past-events-photos .value').fadeIn();
    });
}

function metrics() {
    var start = get_unix_start();
    $.getJSON('ajax/metrics/'+start, function(json){
        // average photo
        $('#metric-avg-event-photos .value').hide();
        $('#metric-avg-event-photos .value').html(json.metrics.avg_photos_per_event.toFixed(2));
        $('#metric-avg-event-photos .value').fadeIn();

        // average guests
        $('#metric-avg-event-guests .value').hide();
        $('#metric-avg-event-guests .value').html(json.metrics.avg_guests_per_event.toFixed(2));
        $('#metric-avg-event-guests .value').fadeIn();

        // revenue
        var net_revenue = json.metrics.orders.amount__sum - json.metrics.orders.amount_refunded__sum;
        $('#metric-revenue .value').hide();
        $('#metric-revenue .value').html('$'+Math.round(json.metrics.orders.amount__sum/100)+' | $'+Math.round(net_revenue/100));
        $('#metric-revenue .value').fadeIn();
    });
}

// time helping function
function get_unix_days(days) {
    var current_unix = Math.round(new Date().getTime() / 1000);
    var days_unix = (current_unix + (days * 86400));
    return days_unix;
}

function get_unix_start() {
    // get current unix
    var current_unix = Math.round(new Date().getTime() / 1000);

    // get the start
    var days = $('#metrics-range form input[name="metrics-range"]:checked').val();
    var start_unix = (days > 0) ? (current_unix - (days * 86400)) : 0;
    return start_unix;
}

function get_unix_end() {
    return Math.round(new Date().getTime() / 1000);
}