//
// A custom jqueryui plugin widget.
// based on: http://jqueryui.com/widget/
//
// This is part of the Chronicle Project.
// It accesses the couchdb database and shows
// various levels of detail.
//
// WIP 2014-01-31


$(function() {

  $.widget( "chronicle.series", {
    // default options
    options: {
      // the chronicle key to the series
      seriesUID: null,

      // the currently selected imageInstanceUID to display
      imageInstanceUID : null,

      // callbacks
      change: null,
    },


    // the constructor
    _create: function() {

      // dicom classes associated with images we can display
      this.imageClasses = [
                "1.2.840.10008.5.1.4.1.1.1", // CR Image
                "1.2.840.10008.5.1.4.1.1.2", // CT Image
                "1.2.840.10008.5.1.4.1.1.4", // MR Image
                "1.2.840.10008.5.1.4.1.1.6", // US Image
                "1.2.840.10008.5.1.4.1.1.7", // SC Image
                "1.2.840.10008.5.1.4.1.1.7.1", // SC Image - bit
                "1.2.840.10008.5.1.4.1.1.7.2", // SC Image - byte
                "1.2.840.10008.5.1.4.1.1.7.3", // SC Image - word
                "1.2.840.10008.5.1.4.1.1.7.4", // SC Image - true color
      ];

      // state variables
      this.pendingSeriesRequest = null;
      this.pendingReferencesRequest = null;

      // the list of image class instance UIDs associated with this seriesUID
      this.imageInstanceUIDs = [];

      // the list of control point class instance UIDs associated with this seriesUID
      this.controlPointInstanceUIDs = [];

      // the image source to fetch from
      this.imgSrc = "";

      // the control point lists for the current instance
      //  - will be a list of lists of points
      this.controlPoints = [];

      // Set the class and disable click
      this.element
        // add a class for theming
        .addClass( "chronicle-series" )
        // prevent double click to select text
        .disableSelection();

      // Add the slice slider
      this.sliceSlider = $( "<input>", {
         "class": "chronicle-series-sliceSlider",
         "id": "sliceSlider",
         "type" : "range",
         "data-role" : "slider",
         "width" : "512px"
      }).appendTo( this.element );

      $( "<br>" ).appendTo( this.element );

      // Add the svg container for the slice (instance)
      this.sliceGraphics = $( "<div>", {
         "class" : "chronicle-series-sliceGraphics",
         "id" : "sliceGraphics",
         "width" : "512px",
         "height" : "512px",
      }).appendTo( this.element );

      $('#sliceGraphics').svg({
        onLoad: this._drawGraphics,
        width: 512,
        height: 512
      });

      $( "<br>" ).appendTo( this.element );

      this._refresh();
    },


    // events bound via _on are removed automatically
    // revert other modifications here
    _destroy: function() {
      // remove generated elements
      this.sliceSlider.remove();
      this.sliceGraphics.remove();

      this._clearResults();

      this.element
        .removeClass( "chronicle-series" )
        .enableSelection();
    },


    _clearResults: function() {
      $('p',this.element[0]).remove();
    },

    // called when created, and later when changing options
    _refresh: function() {

      // clear previous results
      this._clearResults();

      // abort pending requests
      if (this.pendingSeriesRequest) {
        this.pendingSeriesRequest.abort();
        this.pendingSeriesRequest = null;
      }
      if (this.pendingReferencesRequest) {
        this.pendingReferencesRequest.abort();
        this.pendingReferencesRequest = null;
      }

      // create a slider with the max set to the number of instances
      // - when it is manipulated, trigger an update to the instance value
      //   and thus redraw the graphics
      var series = this;
      this.pendingSeriesRequest =
        $.couch.db("chronicle").view("instances/seriesInstances", {
          key : this.options.seriesUID,
          reduce : false,
          success: function(data) {
            series.imageInstanceUIDs = [];
            series.controlPointInstanceUIDs = [];
            $.each(data.rows, function(index,row) {
              var classUID = row.value[0];
              var instanceUID = row.value[1];
              if (series.imageClasses.indexOf(classUID) != -1) {
                series.imageInstanceUIDs.push(instanceUID);
              } else {
                // TODO: once we have a classUID for control points we can do better
                // For now, assume any non-image is a control point list
                series.controlPointInstanceUIDs.push(instanceUID);
              }
            });
            var imageInstanceIndex = series.imageInstanceUIDs.indexOf(
                                               series.options.imageInstanceUID);
            var instanceCount = series.imageInstanceUIDs.length;
            $('#sliceSlider').attr( 'max', instanceCount-1 );
            if (imageInstanceIndex == -1) {
              imageInstanceIndex = Math.round(instanceCount/2);
            }
            $('#sliceSlider').val( imageInstanceIndex );
            series._imageInstanceIndex( imageInstanceIndex );
            $('#sliceSlider').bind("change", function(event,ui) {
                    var value = $('#sliceSlider').val();
                    series._imageInstanceIndex(value);
            });
          },
          error: function(status) {
            console.log(status);
            alert(status);
          },
        });

      // trigger a callback/event
      this._trigger( "change" );
    },

    // called when created, and later when changing options
    // This draws the current image and then sets up a request
    // for all the objects that reference this instance
    // TODO: currently hard-coded for control points and curves
    _imageInstanceIndex: function(index) {

      // draw with the image first, overlays will come later
      this.controlPoints = [];
      this.options.imageInstanceUID = this.imageInstanceUIDs[index];
      this.imgSrc = '../' + this.options.imageInstanceUID + '/image512.png';
      // TODO
      this.options.imageInstanceUID = "1.3.6.1.4.1.35511635209895445060349.1.4.0.3.16";
      //this._drawGraphics();

      // abort pending requests
      if (this.pendingReferencesRequest) {
        this.pendingReferencesRequest.abort();
      }

      // request curve lists associated with this instance
      var series = this;
      this.pendingReferencesRequest =
        $.couch.db("chronicle").view("instances/instanceReferences", {
          key : series.options.imageInstanceUID,
          include_docs : true,
          reduce : false,
          success: function(data) {
            $.each(data.rows, function(index,value) {
              instancePoints = value.doc.instancePoints;
              series.controlPoints.push(instancePoints[series.options.imageInstanceUID]);
            });
            series._drawGraphics();
          },
          error: function(status) {
            console.log(status);
            alert(status);
          },
        });
    },

    _updateLines: function() {
      svg = $('#sliceGraphics').svg('get');
      $('polyline').remove();
      // add lines
      $.each(this.controlPoints, function(index, points) {
        points.push(points[0]); // close the line
        svg.polyline(points,
                     {fill: 'none', stroke: 'yellow', strokeWidth: 1, opacity: 0.5});
      });
    },

    _drawGraphics: function() {

      // clear the old graphics
      svg = $('#sliceGraphics').svg('get');
      svg.clear();

      // draw the image
      if (this.imgSrc) {
        svg.image(null, 0, 0, 512, 512, this.imgSrc);
      }

      // draw the graphic overlay
      if (this.controlPoints) {
	this._updateLines();

        // add control points
        $.each(this.controlPoints, function(curveIndex, points) {
          $.each(points, function(pointIndex, point) {
            circle = svg.circle(point[0], point[1], 5,
                        {fill: 'red', stroke: 'blue', strokeWidth: 1, opacity: 0.5,
                         curveIndex: curveIndex, pointIndex: pointIndex
                        })
          });
        });

        var series = this;
        $('circle')
        .draggable()
        .bind('mouseenter', function(event){
          // bring target to front
          $(event.target.parentElement).append( event.target );
          event.target.setAttribute('opacity', 1.0);
          event.target.setAttribute('stroke', 'green');
        })
        .bind('mouseleave', function(event){
          event.target.setAttribute('opacity', 0.5);
          event.target.setAttribute('stroke', 'blue');
        })
        .bind('mousedown', function(event){
          // record start position offset from center of point
          var dx = event.target.getAttribute('cx') - event.offsetX;
          var dy = event.target.getAttribute('cy') - event.offsetY;
          event.target.setAttribute('dx', dx);
          event.target.setAttribute('dy', dy);
        })
        .bind('drag', function(event, ui){
          // update circle coordinates
          var cx = event.offsetX - event.target.getAttribute('dx');
          var cy = event.offsetY - event.target.getAttribute('dy');
          event.target.setAttribute('cx', cx);
          event.target.setAttribute('cy', cy);
          // update curve in series object
          var curveIndex = event.target.getAttribute('curveIndex');
          var pointIndex = event.target.getAttribute('pointIndex');
          series.controlPoints[curveIndex][pointIndex] = [cx, cy];
          // redraw the lines with new values
          series._updateLines();
        });
      }
    },


    // _setOptions is called with a hash of all options that are changing
    // always refresh when changing options
    _setOptions: function() {
      // _super and _superApply handle keeping the right this-context
      this._superApply( arguments );
      this._refresh();
    },

    // _setOption is called for each individual option that is changing
    _setOption: function( key, value ) {
      // prevent invalid color values
      if ( /red|green|blue/.test(key) && (value < 0 || value > 255) ) {
        return;
      }
      this._super( key, value );
    }
  });

});
