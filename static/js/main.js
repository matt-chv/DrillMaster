(function($) {
  
  var index = 0;
  
  
  $(document).ready(function() {
    $('input[name=side_mode]').click(function() {
      var mapping = null;
      
      switch ($(this).attr('id')) {
        case 'front_value_and_hint':
          mapping = {
            frontValue: 'frontValue',
            backValue:  'backValue',
            frontHint:  'frontHint',
            backHint:   'backHint'
          };
          break;
        case 'front_value':
          mapping = {
            frontValue: 'frontValue',
            backValue:  null,
            frontHint:  null,
            backHint:   null
          };
          break;
        case 'back_only':
          mapping = {
            frontValue: 'backHint',
            backValue:  'backValue',
            frontHint:  null,
            backHint:   null
          };
          break;
      }
      
      $('.flashcardContainer').html('').flashcards({
        sideMapping:   mapping,
        headGenerator: headGenerator,
        footGenerator: footGenerator
      });
      
      $('.flashcardContainer').flashcards('switch-card', cards[index]);
    });
    
    $('input[name=side_mode][checked=checked]').click();
    
    $('button[name=switch]').click(function() {
      index = (++index) % cards.length;
      $('.flashcardContainer').flashcards('switch-card', cards[index]);
    });
    
    $('button[name=turn]').click(function() {
      $('.flashcardContainer').flashcards('turn-card');
    });

    //Next five functions are making an ajax call to the server to:
    //a) inform the server about the self assessed level of memorisation
    //b) based on today's scores, get from the server the next card index
    $('button[name=level0]').click(function() {
      //API v=0: round-robin on card index - no ajax calls
      //index = (++index) % cards.length;
      //API v1.x: GET on REST API to server with current card index and assesment level
      // recovers a json with next_card_index (int) as content
      $.ajax({
        url : '/api/mnemo?card_index=' + index + '&assesment_level=' + 0,
        success: function(data) {
          index=data['next_card_index'];
          //once the next card index is received, update the displayed card to be the one
          //selected by the server side algorithms
          $('.flashcardContainer').flashcards('switch-card', cards[index]);
        }
      })
    });
    $('button[name=level1]').click(function() {
      //index = (++index) % cards.length;
      $.ajax({
        url : '/api/mnemo?card_index=' + index + '&assesment_level=' + 1,
        success: function(data) {
          index=data['next_card_index'];
          console.log("MCV");
          console.log(index)
          $('.flashcardContainer').flashcards('switch-card', cards[index]);
        }
      })
    });
    $('button[name=level2]').click(function() {
      //index = (++index) % cards.length;
      $.ajax({
        url : '/api/mnemo?card_index=' + index + '&assesment_level=' + 2,
        success: function(data) {
          index=data['next_card_index'];
          console.log("MCV");
          console.log(index)
          $('.flashcardContainer').flashcards('switch-card', cards[index]);
        }
      })
    });
    $('button[name=level3]').click(function() {
      //index = (++index) % cards.length;
      $.ajax({
        url : '/api/mnemo?card_index=' + index + '&assesment_level=' + 3,
        success: function(data) {
          index=data['next_card_index'];
          console.log("MCV");
          console.log(index)
          $('.flashcardContainer').flashcards('switch-card', cards[index]);
        }
      })
    });
    $('button[name=level4]').click(function() {
      //index = (++index) % cards.length;
      $.ajax({
        url : '/api/mnemo?card_index=' + index + '&assesment_level=' + 4,
        success: function(data) {
          index=data['next_card_index'];
          console.log("MCV");
          console.log(index)
          $('.flashcardContainer').flashcards('switch-card', cards[index]);
        }
      })
    });

    $('button[name=level5]').click(function() {
      //index = (++index) % cards.length;
      $.ajax({
        url : '/api/mnemo?card_index=' + index + '&assesment_level=' + 5,
        success: function(data) {
          index=data['next_card_index'];
          console.log("MCV");
          console.log(index)
          $('.flashcardContainer').flashcards('switch-card', cards[index]);
        }
      })
    });

    $('button[name=level1]').click(function() {
      index = (++index) % cards.length;
      $('.flashcardContainer').flashcards('switch-card', cards[index]);
    });

    $('button[name=level2]').click(function() {
      index = (++index) % cards.length;
      $('.flashcardContainer').flashcards('switch-card', cards[index]);
    });


  });
  
  
  function headGenerator(side, value, hint) {
    return '#' + (index + 1) + ' - ' + side + ' head'
  }
  
  
  function footGenerator(side, value, hint) {
    return '#' + (index + 1) + ' - ' + side + ' foot'
  };
  
})(jQuery);
