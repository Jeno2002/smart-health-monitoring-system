// Navbar Animation
function test() {
     const tabsNewAnim = $('#navbarSupportedContent');
     const activeItemNewAnim = tabsNewAnim.find('.active');
     const activeHeight = activeItemNewAnim.innerHeight();
     const activeWidth = activeItemNewAnim.innerWidth();
     const itemPos = activeItemNewAnim.position();
 
     $(".hori-selector").css({
         "top": itemPos.top + "px",
         "left": itemPos.left + "px",
         "height": activeHeight + "px",
         "width": activeWidth + "px"
     });
 
     $("#navbarSupportedContent").on("click", "li", function () {
         $('#navbarSupportedContent ul li').removeClass("active");
         $(this).addClass('active');
         const activeHeight = $(this).innerHeight();
         const activeWidth = $(this).innerWidth();
         const itemPos = $(this).position();
 
         $(".hori-selector").css({
             "top": itemPos.top + "px",
             "left": itemPos.left + "px",
             "height": activeHeight + "px",
             "width": activeWidth + "px"
         });
     });
 }
 
 $(document).ready(function () {
     setTimeout(test, 100);
 
     // Add Active Class Based on Path
     const path = window.location.pathname.split("/").pop() || 'index.html';
     const target = $('#navbarSupportedContent ul li a[href="' + path + '"]');
     target.parent().addClass('active');
 });
 
 $(window).on('resize', function () {
     setTimeout(test, 500);
 });
 
 $(".navbar-toggler").click(function () {
     $(".navbar-collapse").slideToggle(300);
     setTimeout(test, 100);
 });

  // Bar Chart Configuration
  var barOptions = {
    chart: {
      type: 'bar',
      height: 300
    },
    series: [{
      name: 'Patients',
      data: [120, 150, 180, 200, 250]
    }],
    xaxis: {
      categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May']
    },
    title: {
      text: 'Monthly New Patients',
      align: 'center',
      style: {
        fontSize: '16px'
      }
    }
  };


  var timelineOptions = {
    chart: {
      type: 'rangeBar',
      height: 300
    },
    series: [{
      name: 'Events',
      data: [{
        x: 'User1 Task',
        y: [new Date('2023-12-01').getTime(), new Date('2023-12-03').getTime()]
      }, {
        x: 'User2 Task',
        y: [new Date('2023-12-02').getTime(), new Date('2023-12-05').getTime()]
      }, {
        x: 'User3 Task',
        y: [new Date('2023-12-04').getTime(), new Date('2023-12-07').getTime()]
      }]
    }],
    xaxis: {
      type: 'datetime'
    },
    title: {
      text: 'Task Timeline',
      align: 'center',
      style: {
        fontSize: '16px'
      }
    }
  };

  // Render the Charts
  var barChart = new ApexCharts(document.querySelector("#bar-chart"), barOptions);
  var timelineChart = new ApexCharts(document.querySelector("#timeline-chart"), timelineOptions);

  barChart.render();
  timelineChart.render();


 