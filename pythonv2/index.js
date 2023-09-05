function getFormattedTimestamp() {
    const options = {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: 'numeric',
      minute: 'numeric',
      second: 'numeric',
      timeZoneName: 'short',
      timeZone: 'UTC'
    };
    
    const timestamp = new Date().toLocaleString('en-US', options);
    return timestamp.replace('GMT', 'UTC');
  }
  
  const formattedTimestamp = getFormattedTimestamp();
  console.log(formattedTimestamp);
  