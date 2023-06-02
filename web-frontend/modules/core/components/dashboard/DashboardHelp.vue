<template>
  <div class="dashboard__help">
    <div class="dashboard__help-title">{{ $t('dashboard.alertTitle') }}</div>
    <p class="dashboard__help-description">
      {{ $t('dashboard.alertText') }}
    </p>

    <Button
      icon="gitlab-full"
      href="https://gitlab.com/baserow/baserow"
      rel="noopener noreferrer"
      target="_blank"
    >
      {{ $t('dashboard.starOnGitlab') }}
    </Button>
    <Button
      v-tooltip="$t('dashboard.shareOnTwitter')"
      icon="twitter"
      :href="
        'https://twitter.com/intent/tweet?url=https://baserow.io' +
        '&hashtags=opensource,nocode,database,baserow&text=' +
        encodeURI($t('dashboard.tweetContent'))
      "
      rel="noopener noreferrer"
      target="_blank"
    >
    </Button>

    <Button
      v-tooltip="$t('dashboard.shareOnReddit')"
      icon="reddit"
      :href="
        'https://www.reddit.com/submit?url=https://baserow.io&title=' +
        encodeURI($t('dashboard.redditTitle'))
      "
      rel="noopener noreferrer"
      target="_blank"
    >
    </Button>

    <Button
      v-tooltip="$t('dashboard.shareOnFacebook')"
      icon="facebook"
      href="https://www.facebook.com/sharer/sharer.php?u=https://baserow.io"
      rel="noopener noreferrer"
      target="_blank"
    >
    </Button>

    <Button
      v-tooltip="$t('dashboard.shareOnLinkedIn')"
      icon="linkedin"
      href="https://www.linkedin.com/sharing/share-offsite/?url=https://baserow.io"
      rel="noopener noreferrer"
      target="_blank"
    >
    </Button>
  </div>
</template>

<script>
export default {
  name: 'DashboardHelp',
}
</script>
