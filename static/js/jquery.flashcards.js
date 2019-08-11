(function($) {
  
  var CLASS = { // CSS classes
    WRAPPER: 'flashcardWrapper',
    CARD:    'flashcard',
    FRONT:   'flashcardFront',
    BACK:    'flashcardBack',
    HEAD:    'flashcardHead',
    FOOT:    'flashcardFoot',
    BODY:    'flashcardBody',
    VALUE:   'flashcardValue',
    HINT:    'flashcardHint'
  }
  
  var SIDE = { // Card sides
    FRONT: 'front',
    BACK:  'back'
  }
  
  $.fn.flashcards = function(arg1, arg2) {
    switch (typeof arg1) {
      case 'undefined':
      case 'object':
        return initialize(this, arg1);
      case 'string':
        switch (arg1) {
          case 'switch-card':
            return switchCard(this, arg2);
          case 'turn-card':
            return turnCard(this);
          default:
            return;
        }
    }
  };
  
  function initialize(container, settings) {
    var defaultsideMapping = {
      frontValue: 'frontValue',
      frontHint:  'frontHint',
      backValue:  'backValue',
      backHint:   'backHint'
    };
    
    container.data('settings', $.extend({
      questionSide:  SIDE.FRONT,
      sideMapping:       defaultsideMapping,
      headGenerator: function(side, value, hint) { return '' },
      footGenerator: function(side, value, hint) { return '' }
    }, settings));
    
    var wrapper = $('<div>').addClass(CLASS.WRAPPER);
    container.append(wrapper);
    container.data('wrapper', wrapper);
    
    return container;
  }
  
  function switchCard(container, data) {
    var settings = container.data('settings');
    var card = createCard(settings, data);
    container.data('wrapper').html(card);
    return container;
  }
  
  function createCard(settings, data) {
    var cardData = $.extend({
      frontValue: '',
      frontHint:  '',
      backValue:  '',
      backHint:   ''
    }, data);
    
    var frontValue = (settings.sideMapping.frontValue) ? cardData[settings.sideMapping.frontValue] : null;
    var frontHint = (settings.sideMapping.frontHint) ? cardData[settings.sideMapping.frontHint] : null;
    var backValue = (settings.sideMapping.backValue) ? cardData[settings.sideMapping.backValue] : null;
    var backHint = (settings.sideMapping.backHint) ? cardData[settings.sideMapping.backHint] : null;

    var front = createSide(settings, SIDE.FRONT, frontValue, frontHint);
    var back = createSide(settings, SIDE.BACK, backValue, backHint);
    var card = $('<div>').addClass(CLASS.CARD);
    card.append(front).append(back);
    
    if (settings.questionSide = SIDE.FRONT) {
      back.hide();
    } else {
      front.hide();
    }
    
    return card;
  }

  function createSide(settings, type, value, hint) {
    var side = $('<div>');
    
    if (type == SIDE.FRONT) {
      side.addClass(CLASS.FRONT);
    } else {
      side.addClass(CLASS.BACK);
    }
    
    var sideHeader = $('<div>').addClass(CLASS.HEAD).html(
      settings.headGenerator(type, value, hint));
    
    var sideBody = $('<div>').addClass(CLASS.BODY);
    var sideValue = $('<div>').addClass(CLASS.VALUE).html(value);
    sideBody.append(sideValue);
    
    if (hint !== null && hint !== undefined && hint.length > 0) {
      var sideHint = $('<div>').addClass(CLASS.HINT).html(hint);
      sideBody.append(sideHint);
    }

    var sideFooter = $('<div>').addClass(CLASS.FOOT).html(
      settings.footGenerator(type, value, hint));
    
    side.append(sideHeader).append(sideBody).append(sideFooter);

    return side;
  }

  function evaluatePossibleCallback(callback, value, hint) {
    if (typeof callback === 'function') {
      return callback(value, hint);
    } else {
      return callback;
    }
  }
  
  function turnCard(container) {
    var wrapper = $(container).data('wrapper');
    wrapper.find('.' + CLASS.FRONT).toggle();
    wrapper.find('.' + CLASS.BACK).toggle();
    return container;
  }
 
})(jQuery);
