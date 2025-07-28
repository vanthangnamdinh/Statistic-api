CREATE TABLE statistic_logs (
    user String,                                 -- Id of User
    message_id String,                           -- ID of message
    conversation_id String,                      -- Id of conversation
    timestamp_chat DateTime,                     -- Time of message
    statistic_data_url String,                                  -- URL of browser when User sends a message
    statistic_data_page_title String,                           -- Page title
    statistic_data_page_metadata String,                        -- JSON metadata of the page as String
    statistic_data_page_keywords Array(String),                 -- Array of strings (page keywords)
    statistic_data_session_history_url Array(String),           -- Array of history URLs
    statistic_data_focus_content_snippet String,                -- JSON snippet of current focus content as String
    statistic_data_reading_duration_ms UInt64,                  -- Reading duration in milliseconds
    statistic_data_cookies String,                              -- JSON cookies as String
    error_message String                                        -- Error response returned by the BE
) 
ENGINE = MergeTree() 
ORDER BY (timestamp_chat, user);