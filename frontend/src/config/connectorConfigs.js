export const CONNECTOR_CONFIGS = {

  youtube: [

    {
      name: "api_key",
      label: "YouTube API Key",
      type: "text"
    },

    {
      name: "keywords",
      label: "Keywords",
      type: "text"
    },

    {
      name: "max_videos",
      label: "Max Videos",
      type: "number",
      defaultValue: 20
    },

    {
      name: "max_comments",
      label: "Max Comments",
      type: "number",
      defaultValue: 100
    }

  ],

  instagram_account: [

    {
      name: "access_token",
      label: "Access Token",
      type: "text"
    },

    {
      name: "ig_user_id",
      label: "Instagram Business Account ID",
      type: "text"
    },

    {
      name: "max_posts",
      label: "Max Posts",
      type: "number",
      defaultValue: 100
    }

  ],

  instagram_hashtag: [

    {
      name: "access_token",
      label: "Access Token",
      type: "text"
    },

    {
      name: "ig_user_id",
      label: "Instagram Business Account ID",
      type: "text"
    },

    {
      name: "hashtags",
      label: "Hashtags",
      type: "text"
    },

    {
      name: "max_posts",
      label: "Max Posts",
      type: "number",
      defaultValue: 500
    }

  ],

  reddit: [

    {
      name: "keywords",
      label: "Keywords",
      type: "text"
    },

    {
      name: "post_limit",
      label: "Post Limit",
      type: "number",
      defaultValue: 100
    }

  ],

  newsapi: [

        {
        name: "api_key",
        label: "News API Key",
        type: "text"
        },

        {
        name: "keywords",
        label: "Keywords",
        type: "text"
        }

    ],
    campaignindia: [

    {
        name: "keywords",
        label: "Keywords (comma separated)",
        type: "text"
    },

    {
        name: "max_articles",
        label: "Max Articles Per Keyword",
        type: "number",
        defaultValue: 50
    }

    ],
    googlenews: [

    {
        name: "keywords",
        label: "Keywords",
        type: "text"
    },

    {
        name: "max_articles",
        label: "Max Articles",
        type: "number",
        defaultValue: 100
    }

    ],
    newsapi: [

    {
      name: "api_key",
      label: "News API Key",
      type: "text"
    },

    {
      name: "keywords",
      label: "Keywords",
      type: "text"
    },

    {
      name: "language",
      label: "Language",
      type: "text",
      defaultValue: "en"
    },

    {
      name: "max_articles",
      label: "Max Articles",
      type: "number",
      defaultValue: 100
    }

  ],
    rss_reviews: [

    {
      name: "rss_urls",
      label: "RSS Feed URLs",
      type: "textarea"
    }

  ]

};