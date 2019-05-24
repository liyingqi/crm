$('.item .title').click(function () {
   $(this).next().removeClass('hide').parent().siblings().find('.body').addClass('hide');
});