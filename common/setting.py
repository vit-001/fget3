# -*- coding: utf-8 -*-
__author__ = 'Vit'


class Setting:
    cache_path = 'common/cashe/'
    thumbs_cache_path=cache_path+'thumbs/'
    pictures_path=cache_path+'pictures/'
    data_server_config_path = 'common/locals/'
    global_data_path = 'common/globals/'

    main_window_x0_in_percents = 2
    main_window_y0_in_percents = 5
    main_window_h_in_percents = 75
    main_window_w_in_pixels = 458

    full_window_x1_in_percents = 2
    full_window_y0_in_percents = 5
    full_window_h_in_percents = 75
    full_window_w_gap_in_percents = 2

    log_window_x1_in_percents = 2
    log_window_y0_in_percents = 84
    log_window_h_in_percents = 10
    log_window_w_gap_in_percents = 2

    debug_site=True
    debug_view=True
    debug_loader=True

    site_statistic=True

if __name__ == "__main__":
    pass
