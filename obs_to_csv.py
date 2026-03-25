import georinex as gr
import pandas as pd

def obs_to_csv(obs_path: str, csv_path: str):

    obs = gr.load(obs_path)

    # ---- 観測タイプの取得 ----
    if hasattr(obs, "obs"):
        # DataArray: obs.obs は観測タイプ一覧
        obs_types = list(obs.obs.values)
    else:
        # Dataset: data_vars が観測タイプ
        obs_types = list(obs.data_vars.keys())

    print("観測タイプ:", obs_types)

    # ---- time, sv 取得 ----
    times = obs.time.values
    svs = obs.sv.values

    rows = []

    # Dataset と DataArray で処理分け
    if hasattr(obs, "obs"):
        # DataArray（time, sv, obs_type）
        for t_idx, t in enumerate(times):
            df = obs.isel(time=t_idx).to_pandas()
            df["time"] = t
            rows.append(df.reset_index())

    else:
        # Dataset：各観測タイプが独立した DataArray
        for t_idx, t in enumerate(times):
            row = {"time": t}
            for sv in svs:
                row_sv = {"time": t, "sv": sv}
                for obs_type in obs_types:
                    val = obs[obs_type].isel(time=t_idx).sel(sv=sv).values
                    row_sv[obs_type] = float(val) if val is not None else None
                rows.append(row_sv)

    df_all = pd.DataFrame(rows)
    df_all.to_csv(csv_path, index=False)
    print(f"Saved: {csv_path}")


if __name__ == "__main__":
    obs_to_csv("OIRIbase.obs", "obs_alldata.csv")
