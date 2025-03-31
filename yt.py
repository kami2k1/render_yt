import subprocess
def get_gpu_encoder():
    """
    Xác định bộ mã hóa GPU tốt nhất có sẵn cho ffmpeg.
    
    Returns:
        str: Tên của bộ mã hóa sẽ sử dụng.
    """
    try:
        output = subprocess.check_output(["ffmpeg", "-encoders"], stderr=subprocess.DEVNULL).decode()
        if "h264_nvenc" in output:
            return "h264_nvenc"  # NVIDIA GPU
        elif "h264_qsv" in output:
            return "h264_qsv"  # Intel QuickSync
        elif "h264_vaapi" in output:
            return "h264_vaapi"  # AMD VAAPI
    except:
        pass
    return "h264"  # CPU
GPU_ENCODER = get_gpu_encoder()

import yt_dlp
import os
import concurrent.futures
import re
thread = concurrent.futures.ThreadPoolExecutor(2) # tăng thread ở đây
def sart():
                output_dir = "out"
                path_render = "video"
                kami = input("16:9 or 9:16? (Nhập 'y' nếu muốn 16:9, ngược lại sẽ là 9:16): ").strip().lower()
                kami = kami == 'y'  # Nếu nhập 'y' thì kami = True, ngược lại False
                name_video = input(str("name file vd 1 , 2 ,3 nó sẽ nghi đè lưu ý: "))
                path = f"{path_render}/{name_video}.mp4"
                os.makedirs(output_dir, exist_ok=True)
                os.makedirs(path_render, exist_ok=True)
                import shutil

                if os.path.exists(output_dir):
                    try:
                        shutil.rmtree(output_dir)
                    except:
                        ""
                
                link_list = {
                    "url": [],
                }
                cmd_df = {}
                for _ in range(99):
                    l = input(f"Nhập link {_+1}: ").strip()
                    if l:
                        link_list["url"].append(l)
                        link_list[l] = {"t": 0, "d": False}
                        cmd_df[_] = {"st":0, "end":10, "id":_}
                    else:
                        break
                def get_time(st):
                    if "p" in st:
                        match = re.match(r"(\d+)p(\d+)", st)
                        if match:
                            minutes, seconds = map(int, match.groups())
                            return minutes * 60 + seconds
                    elif st.isdigit():
                        return int(st)
                    return None
                cmd = {}
                print("\nCấu hình nâng cao (Enter để mặc định cắt 10s đầu)")

                for _ in range(99):
                    ln = input("Nhập video ID: ").strip()
                    if not ln:
                        break
                    
                    ln = int(ln) - 1
                    if ln >= len(link_list["url"]) and ln >=0:
                        print("Không tồn tại ID đó!")
                        continue
                    
            
                    st = get_time(input("Thời gian bắt đầu cắt (vd: 1 ,2 , 2p2): ").strip()) or 0
                    end = get_time(input("Thời gian kết thúc (mặc định 10s): ").strip()) or 10

                    cmd[_] = {"id": ln, "st": st, "end": end}

                
                

                def dow_for_url(url: str, video_id: str):
                    
                    try:
                        with yt_dlp.YoutubeDL() as ydl:
                            info = ydl.extract_info(url, download=False)
                            duration = info.get("duration", 0)

                        config = {
                            "format": "bestvideo+bestaudio",
                            "outtmpl": os.path.join(output_dir, f"{video_id}.mp4"),
                            "merge_output_format": "mp4",
                            "quiet": True,
                            "overwrites": True,
                                "no_warnings": True,  
                                "logger": None,
                                 "cookies_from_browser": ("chrome",),
                        }

                        with yt_dlp.YoutubeDL(config) as ydl:
                            ydl.download([url])

                        
                        link_list[url] = {"t": duration, "d": True}
                        print(duration)
                    except Exception as e:
                        ""
                       

               
                def getallvideo(link_list):
                    futures = {
                        thread.submit(dow_for_url, url, str(i)): url
                        for i, url in enumerate(link_list["url"])
                    }

                    for future in concurrent.futures.as_completed(futures):
                        try:
                            future.result()
                        except Exception as e:
                           ""
                
                def capcut():
                    filter_complex = []
                    index = 0
                    cmds = cmd if len(cmd) >=1 else cmd_df
                    for key, itme in cmds.items():
                        id = itme["id"]
                        url = link_list["url"][id]
                        t = link_list[url]["t"]
                        d = link_list[url]["d"]
                        if not d:
                            print(f" Bỏ qua video {url} vì tải thất bại.")
                            continue
                        
                        st = itme["st"]
                        end = itme["end"]
                        if st > t:
                            print(f"Bỏ qua video {url} vì thời gian cắt vượt quá độ dài video.")
                            continue
                        if end > t or end == -1:
                            end = t

                        
#                         filter_complex.append(
#     f"[{id}:v]trim=start={st}:end={end},setpts=PTS-STARTPTS,"
#     f"scale=w=1080:h=-2:flags=lanczos,"
#     f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black[v{index}]"
# )
                        if kami:

                                filter_complex.append(
                                    f"[{id}:v]trim=start={st}:end={end},setpts=PTS-STARTPTS,"
                                    f"scale=w=1920:h=-2:flags=lanczos,"
                                    f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black[v{index}]"
    )                           
                        else:

                             filter_complex.append(
                                                f"[{id}:v]trim=start={st}:end={end},setpts=PTS-STARTPTS,"
                                                f"scale=w=1080:h=-2:flags=lanczos,"
                                                f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black[v{index}]"
    )
                        filter_complex.append(f"[{id}:a]atrim=start={st}:end={end},asetpts=PTS-STARTPTS[a{index}]")
                        index += 1
                    concat_str = "".join([f"[v{i}][a{i}]" for i in range(index)]) + f"concat=n={index}:v=1:a=1[outv][outa]"
                    filter_complex.append(concat_str)

                    gpu = f"-hwaccel {"cuda" if GPU_ENCODER == "h264_nvenc" else "auto"}"
                    input_files = " ".join([
                        f"-hwaccel auto -i {output_dir}/{i}.mp4"
                        for i, url in enumerate(link_list["url"])
                        if link_list[url]["d"]  
                    ])
                    filter_str = " ; ".join(filter_complex)
                    ffmpeg_cmd = f'ffmpeg {input_files} -c:v {GPU_ENCODER} -filter_complex "{filter_str}" -map "[outv]" -map "[outa]" {path} -y'

                    print("\n Đang chạy FFmpeg...")
                    os.system(ffmpeg_cmd)
                    


                getallvideo(link_list)
                capcut()
while True:
    sart()

