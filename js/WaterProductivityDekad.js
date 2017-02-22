var VisPar_AGBPy = {"opacity":0.85,"bands":["b1"],"min":0,"max":12000,"palette":["f4ffd9","c8ef7e","87b332","566e1b"]};
var VisPar_ETay = {"opacity":0.85,"bands":["b1"],"min":0,"max":2000,"palette":["d4ffc6","beffed","79c1ff","3e539f"]};
var VisPar_WPbm = {"opacity":0.85,"bands":["b1"],"min":0,"max":1.2,"palette":["bc170f","e97a1a","fff83a","9bff40","5cb326"]};

var app = {};

app.calcoliGEE = function(){
 
  var L1_AGBPSelected = app.collAGBPFiltered;
  var L1_AETSelected = app.collAETFiltered;
  
  //Above Ground Biomass Production with masked NoData (pixel < 0)
  var L1_AGBPMasked = L1_AGBPSelected.map(function(image){return image.updateMask(image.gte(0))});

  //sum the two cumulated seasons to get annual AGBP, and multiply by 10 to get kgDM/ha
  var L1_AGBPSummedDekad = L1_AGBPMasked.sum(); // .multiply(10); the multiplier will need to be applied on net FRAME delivery, not on sample dataset

  //Actual Evapotranspiration with valid ETa values (>0 and <254)
  var ETaCollMasked = L1_AETSelected.map(function(image) {return image.updateMask(image.lt(254).and(image.gt(0)))});
  
  //add image property (days in dekad) as band
  var ETaColl2 = ETaCollMasked.map(function(image){return image.addBands(image.metadata('days_in_dk'))});
  
  //get ET value, divide by 10 (as per FRAME spec) to get daily value, and multiply by number of days in dekad summed annuallyS
  var ETaColl3 = ETaColl2.map(function ETdk(image){return image.select('b1').divide(10).multiply(image.select('days_in_dk'))}).sum();

  //scale ETsum from mm/m² to m³/ha for WP calculation purposes
  var ETaTotm3 = ETaColl3.multiply(10);

  //calculate biomass water productivity and add to map
  var WPbm = L1_AGBPSummedDekad.divide(ETaTotm3);
  
  var dataPlot = app.controlli.startDate.getValue() + "/" + app.controlli.endDate.getValue();
                      
  //Map.addLayer(L1_AGBPSummedDekad, VisPar_AGBPy, 'AGBP ' + dataPlot,false);
  //Map.addLayer(ETaColl3, VisPar_ETay, 'ETa' + dataPlot ,false);
  Map.addLayer(WPbm,VisPar_WPbm,'BWp' + dataPlot);

};

app.interfaccia = function() {

/* The introduction section. */
  app.presentazione = {
    panel: ui.Panel([
      ui.Label({
        value: 'AGBP Explorer',
        style: {fontWeight: 'bold', fontSize: '24px', margin: '10px 5px'}
      }),
      ui.Label('This app allows you to filter Above Ground Biomass Production and Actual Evapotranspiration collections.')
    ])
  }; 

  /* The collection filter controls. */
  app.controlli = {
    startDate: ui.Textbox('YYYY-MM-DD', '2015-01-01'),
    endDate: ui.Textbox('YYYY-MM-DD', '2015-01-30'),
    selezionaRastersButton: ui.Button('Select Rasters', app.selezioneInputs),
    selectAGBP: ui.Select({
      placeholder: 'Select AGBP image',
      disabled: true
    }),
    selectAET: ui.Select({
      placeholder: 'Select AET image',
      disabled: true
    }),
    loadingLabel: ui.Label({
      value: 'Loading...',
      style: {stretch: 'vertical', color: 'gray', shown: false}
    }),
    calcolaWPButton: ui.Button({
                  label: 'Calculate WP',
                  disabled : true,
                  onClick: function(){
                      if (app.computedIdsAGBP || app.computedIdsAET ) {
                              app.calcoliGEE();
                      }
                  }})
  };
  
  app.pannelli = ui.Panel({
    widgets:[
      ui.Label('Start Date'),app.controlli.startDate,
      ui.Label('End Date'),app.controlli.endDate,
      app.controlli.selezionaRastersButton,
      app.controlli.selectAGBP,
      app.controlli.selectAET,
      app.controlli.calcolaWPButton
      ]
  })
};

app.datasetsSettaggiGenerali = function() {
  
  app.COLLECTION_ID_AGBP = 'projects/fao-wapor/L1_AGBP250';
  app.COLLECTION_ID_AET = 'users/lpeiserfao/AET250';
  app.SECTION_STYLE = {margin: '20px 0 0 0'};
  app.IMAGE_COUNT_LIMIT = 10;
  
};

app.setAttivazioneControlli = function(enabled) {
    
    // Set the loading label visibility to the enabled mode.
    app.controlli.loadingLabel.style().set('shown', enabled);
    
    // Set each of the widgets to the given enabled mode.
    var loadDependentWidgets = [
      app.controlli.selectAET,
      app.controlli.selectAGBP,
      app.controlli.calcolaWPButton
    ];
    
    loadDependentWidgets.forEach(function(widget) {
      widget.setDisabled(enabled);
    });
    
  };

app.selezioneInputs = function(){

  app.setAttivazioneControlli(true);
  
  var collAGBP = ee.ImageCollection(app.COLLECTION_ID_AGBP);
  var collAET = ee.ImageCollection(app.COLLECTION_ID_AET);
  
  Map.centerObject(collAGBP.first(), 4);

  // Set filter variables.
  var start = app.controlli.startDate.getValue();
  if (start) start = ee.Date(start);
  
  var end = app.controlli.endDate.getValue();
  if (end) end = ee.Date(end);

  //if (start) filtered = filtered.filterDate(start, end);
  if (start) app.collAGBPFiltered = collAGBP.filterDate(start, end)
                  .sort('system:time_start', true);
  
  // Convert the collection to a list and get the number of images.
  var size = app.collAGBPFiltered.toList(100).length();
  print('Number of images: ', size);
  
  if (start) app.collAETFiltered = collAET.filterDate(start, end)
                  .sort('system:time_start', true);
    
  // Get the list of computed ids.
  app.computedIdsAGBP = app.collAGBPFiltered
      .limit(app.IMAGE_COUNT_LIMIT)
      .reduceColumns(ee.Reducer.toList(), ['id_no'])
      .get('list');
  
  app.computedIdsAGBP.evaluate(function(ids) {
      app.setAttivazioneControlli(false);
      app.controlli.selectAGBP.items().reset(ids);
      // Default the image picker to the first id.
       app.controlli.selectAGBP.setValue(app.controlli.selectAGBP.items().get(0));
  });
    
  app.computedIdsAET = app.collAETFiltered
      .limit(app.IMAGE_COUNT_LIMIT)
      .reduceColumns(ee.Reducer.toList(), ['system:index'])
      .get('list');
  
  app.computedIdsAET.evaluate(function(ids) {
    // Update the image picker with the given list of ids.
    app.setAttivazioneControlli(false);
    app.controlli.selectAET.items().reset(ids);
    // Default the image picker to the first id.
     app.controlli.selectAET.setValue(app.controlli.selectAET.items().get(0));
  });
}

app.inizializzazione = function() {
  app.interfaccia();
  app.datasetsSettaggiGenerali();
  //app.selezioneInputs();
  //app.calcoliGEE();
  var main = ui.Panel({
    widgets:[
      app.pannelli,
      ],
      style: {width: '320px', padding: '8px'}
  });
  ui.root.insert(0,main);
};

app.inizializzazione();