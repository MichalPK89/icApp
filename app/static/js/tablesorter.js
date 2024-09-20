$(function () {
    var $table = $('table').tablesorter({
        theme: 'blue',
        widgets: ["zebra", "filter"],
        widgetOptions: {
            filter_external: '.search',
            filter_defaultFilter: { 1: '~{query}' },
            filter_columnFilters: true,
            filter_placeholder: { search: 'Search...' },
            filter_saveFilters: true,
            filter_reset: '.reset'
        }
    });

    $('button[data-column]').on('click', function () {
        var $this = $(this),
            totalColumns = $table[0].config.columns,
            col = $this.data('column'),
            filter = [];

        filter[col === 'all' ? totalColumns : col] = $this.text();
        $table.trigger('search', [filter]);
        return false;
    });
});
