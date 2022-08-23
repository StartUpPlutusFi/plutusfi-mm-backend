bigone_schedule = {
    "run-open-every-1-min": {
        "task": "apps.autotrade.tasks.bigone_auto_trade_open_1m",
        "schedule": 60,
    },
    "run-close-every-1-min": {
        "task": "apps.autotrade.tasks.bigone_auto_trade_close_1m",
        "schedule": 60,
    },
    "run-open-every-5-min": {
        "task": "apps.autotrade.tasks.bigone_auto_trade_open_5m",
        "schedule": 5 * 60,
    },
    "run-close-every-5-min": {
        "task": "apps.autotrade.tasks.bigone_auto_trade_close_5m",
        "schedule": 5 * 60,
    },
    "run-open-every-15-min": {
        "task": "apps.autotrade.tasks.bigone_auto_trade_open_15m",
        "schedule": 15 * 60,
    },
    "run-close-every-15-min": {
        "task": "apps.autotrade.tasks.bigone_auto_trade_close_15m",
        "schedule": 15 * 60,
    },
    "run-open-every-30-min": {
        "task": "apps.autotrade.tasks.bigone_auto_trade_open_30m",
        "schedule": 30 * 60,
    },
    "run-close-every-30-min": {
        "task": "apps.autotrade.tasks.bigone_auto_trade_close_30m",
        "schedule": 30 * 60,
    },
    "run-open-every-1-hour": {
        "task": "apps.autotrade.tasks.bigone_auto_trade_open_1h",
        "schedule": 60 * 60,
    },
    "run-close-every-1-hour": {
        "task": "apps.autotrade.tasks.bigone_auto_trade_close_1h",
        "schedule": 60 * 60,
    },
    "run-open-every-4-hours": {
        "task": "apps.autotrade.tasks.bigone_auto_trade_open_4h",
        "schedule": 240 * 60,
    },
    "run-close-every-4-hours": {
        "task": "apps.autotrade.tasks.bigone_auto_trade_close_4h",
        "schedule": 240 * 60,
    },
    "run-open-every-12-hours": {
        "task": "apps.autotrade.tasks.bigone_auto_trade_open_12h",
        "schedule": 720 * 60,
    },
    "run-close-every-12-hours": {
        "task": "apps.autotrade.tasks.bigone_auto_trade_close_12h",
        "schedule": 720 * 60,
    },
    "run-open-every-1-day": {
        "task": "apps.autotrade.tasks.bigone_auto_trade_open_1d",
        "schedule": 1440 * 60,
    },
    "run-close-every-1-day": {
        "task": "apps.autotrade.tasks.bigone_auto_trade_close_1d",
        "schedule": 1440 * 60,
    },
}
