# https://plot.ly/python/gantt/
# https://megatenpa.com/python/plotly/px/gantt-charts/#color
# http://hxn.blog.jp/archives/9505573.html
# programming by N.Goto

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px


def main(graph_type='px') -> None:
    # データ
    df = pd.DataFrame([
        dict(Task='アンケート', Start='2022-10-01', Finish='2022-10-31', Resource='理事会'),
        dict(Task='コンサル選定', Start='2022-09-01', Finish='2022-12-10', Resource='理事会'),
        dict(Task='仕様書作成', Start='2023-01-15', Finish='2023-07-25', Resource='設計施工管理'),
        dict(Task='施工業者選定', Start='2023-08-01', Finish='2023-11-15', Resource='理事会'),
        dict(Task='着工準備', Start='2023-11-15', Finish='2024-01-15', Resource='施工業者'),
        dict(Task='施工管理', Start='2024-01-15', Finish='2024-10-20', Resource='設計施工管理'),
        dict(Task='修繕工事実施', Start='2024-01-15', Finish='2024-10-20', Resource='施工業者'),
    ])

    if graph_type == 'px':
        plot_by_plotly(df)
    else:
        plot_by_mpl(df)


def plot_by_plotly(df) -> None:
    """ plotlyによるガントチャート """
    fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task", color="Resource",
                      title='第2回大規模修繕工事 工程表（案）（2022年9月〜2024年11月）', height=450, width=950)
    # グラフ全体とホバーのフォントサイズ変更
    fig.update_layout(font_size=14, hoverlabel_font_size=14, hoverlabel_font_color='white',
                      xaxis_title='工程', yaxis_title='作業項目',
                      xaxis_title_font_size=14, yaxis_title_font_size=14)
    # 枠線とグリッド線の設定（x軸グリッドは5日表示=5x24x60x60x1000）
    fig.update_xaxes(linecolor='black', gridcolor='gray',
                     mirror=True, tickformat="%y/%m", dtick='M2')
    fig.update_yaxes(linecolor='black', gridcolor='gray', mirror=True, autorange='reversed')
    # ガントチャート表示
    fig.show()


def df_to_list(df) -> list:
    """ DataFrameをリストに変換 """
    data_list = df.values.tolist()
    return data_list


def plot_by_mpl(df) -> None:
    """ 無理やりmatplotlibでガントチャート 
    https://qiita.com/11kenterada/items/22537eeab6e5f1acccfe
    """
    # DataFrameをlistに変換。
    data_list = df_to_list(df)
    data_list.reverse()
    # データの取り出し。
    titles, start, end, res = list(zip(*data_list))
    print(titles)

    # pyplot内でDatesとして扱われるように変換
    edate, bdate = [mdates.date2num(item) for item in (end, start)]
    # 日本語に対応
    plt.rcParams['font.family'] = 'Ricty Diminished'

    fig, ax = plt.subplots(figsize=(12, 6))
    # タイトル領域
    fig.subplots_adjust(left=0.1, right=0.95)
    # 作図
    ax.barh(y=titles, width=edate - bdate, left=bdate, height=0.5)
    #  横軸目盛の表示形式をdateに変更する
    ax.xaxis_date()
    # グリッド線をグラフの後面に表示する
    ax.set_axisbelow(True)
    ax.grid()

    # 描画
    plt.savefig("hoge.png")
    plt.show()


if __name__ == "__main__":
    """ matplotlibでグラフ表示の場合は、main('plt')とする。 """
    main()
