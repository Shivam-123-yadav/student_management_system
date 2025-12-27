'use strict';

$(document).ready(function() {

	// Area chart - Revenue Chart
	
	if ($('#apexcharts-area').length > 0) {
	// Parse chart data from Django context
	var chartDataElement = document.getElementById('chart-data');
	var chartData = chartDataElement ? JSON.parse(chartDataElement.textContent) : null;
	
	var categories = chartData ? chartData.categories : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'];
	var revenueData = chartData ? chartData.revenue : [5000, 6000, 5500, 7000, 6500, 8000, 7500];
	
	var options = {
		chart: {
			height: 350,
			type: "area",
			toolbar: {
				show: false
			},
		},
		dataLabels: {
			enabled: false
		},
		stroke: {
			curve: "smooth"
		},
		series: [{
			name: "Revenue",
			color: '#2196F3',
			data: revenueData
		}],
		xaxis: {
			categories: categories,
		},
		yaxis: {
			title: {
				text: 'Revenue ($)'
			}
		}
	}
	var chart = new ApexCharts(
		document.querySelector("#apexcharts-area"),
		options
	);
	chart.render();
	}

	// Bar chart - Number of Students Chart
	
	if ($('#bar').length > 0) {
	// Parse chart data from Django context (same data element used for multiple charts)
	var chartDataElement = document.getElementById('chart-data');
	var chartData = chartDataElement ? JSON.parse(chartDataElement.textContent) : null;
	
	// For admin dashboard, use students data from the monthly data
	var categories = chartData && chartData.categories ? chartData.categories : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul'];
	var studentsData = chartData && chartData.students ? chartData.students : [20, 30, 25, 35, 30, 40, 35];
	
	var optionsBar = {
		chart: {
			type: 'bar',
			height: 350,
			width: '100%',
			stacked: false,
			toolbar: {
				show: false
			},
		},
		dataLabels: {
			enabled: false
		},
		plotOptions: {
			bar: {
				columnWidth: '45%',
			}
		},
		series: [{
			name: "Number of Students",
			color: '#19affb',
			data: studentsData,
		}],
		xaxis: {
			categories: categories,
		},
		yaxis: {
			axisBorder: {
				show: false
			},
			axisTicks: {
				show: false
			},
			labels: {
				style: {
					colors: '#777'
				}
			},
			title: {
				text: 'Student Count'
			}
		},
		title: {
			text: '',
			align: 'left',
			style: {
				fontSize: '18px'
			}
		}

	}
  
	var chartBar = new ApexCharts(document.querySelector('#bar'), optionsBar);
	chartBar.render();
	}
  
});