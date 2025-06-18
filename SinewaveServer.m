esp32_ip = 'http://192.168.1.29/sine';  % ESP32 local IP endpoint
upload_url = 'https://esp32-emg-1.onrender.com/upload';  % 🔁 Replace this with your Render domain

while true
    try
        % Step 1: Get sinewave data from ESP32
        response = webread(esp32_ip);  
        sinewave = str2double(split(response, ','));  

        % Step 2: Prepare data struct
        data = struct( ...
            'timestamp', datestr(now, 'yyyy-mm-dd HH:MM:SS'), ...
            'sine', sinewave ...
        );

        % Step 3: Send to Render via POST
        options = weboptions('MediaType', 'application/json');
        response = webwrite(upload_url, data, options);

        % Optional plot locally
        plot(sinewave);
        ylim([-1.2 1.2]);
        title("Live Sinewave from ESP32 → Render");
        drawnow;

    catch ME
        warning("⚠️ Error: %s", ME.message);
    end
    pause(1);  % Every 1 second
end
