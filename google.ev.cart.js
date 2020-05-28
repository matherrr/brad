/* Legacy: Local-Shop-AN(Google)-CM-AddToCart */
/* Event snippet for 장바구니 conversion page
In your html page, add the snippet and call gtag_report_conversion when someone clicks on the chosen link or button. */
<script>
function gtag_report_conversion(url) {
  var callback = function () {
    if (typeof(url) != 'undefined') {
      window.location = url;
    }
  };
  gtag('event', 'conversion', {
      'send_to': 'AW-805732128/M2A-CIjSzYEBEKD-mYAD',
      'event_callback': callback
  });
  return false;
}
</script>