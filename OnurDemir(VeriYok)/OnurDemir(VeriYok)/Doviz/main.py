# -*- coding: utf-8 -*-
import os, sys
try:
    from tkinter import *
    import tkinter
    import json
    import datetime, time
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure

    sys.dont_write_bytecode = True

    def restart_program():
        os.execv(sys.executable, ['python'] + sys.argv)

    def frleft_yenile_buton():
        from result_correction import correction
        from API_Request import requesting
        requesting()
        correction()
        restart_program()

    def frmid_tarih():
        try:
            with open("corrected-Result.json", "r") as cr:
                cr_veri = json.load(cr)
                tam_tarih = cr_veri["time_last_update_utc"]
                tarih = tam_tarih[5:16]
                return tarih
        except:
            return 0

    def frtop_right_Label():
        for widget in frtop_right.winfo_children():
                if isinstance(widget, Label):
                    widget.destroy()
        try:
            with open("corrected-Result.json", "r") as cr:
                cr_veri = json.load(cr)
                with open("varlik.json", "r") as d:
                    veri_deneme = json.load(d)
                    birim_toplamlari = []
                    keys_list = list(veri_deneme.keys())
                    keys_list.sort()
                    for key_d in keys_list:
                        for key_cr in list(cr_veri["conversion_rates"].keys()):
                            if key_cr == key_d:
                                d_values = []
                                inside_keys = list(veri_deneme[key_d].keys())
                                for inside_key in inside_keys:
                                    d_values.append(veri_deneme[key_d][inside_key]["Miktar"])
                                d_values = list(cr_veri["conversion_rates"][key_cr]*x for x in d_values)
                                birim_toplamlari.append(sum(d_values))
                    toplam_varlik = sum(birim_toplamlari)
            toplam_varlik_lbl = Label(frtop_right, text="Toplam Varlık:\n{:.2f} TL".format(toplam_varlik), font=25, bg="#FFD494")
            toplam_varlik_lbl.pack(padx=5,pady=22)
        except:
            toplam_varlik_lbl = Label(frtop_right, text="Toplam Varlık:\n0 TL", font=25, bg="#FFE194")
            toplam_varlik_lbl.pack(padx=5,pady=22)   

    def frtop_bt_left_func():
        for widget in frtop.winfo_children():
            if isinstance(widget, Label):
                widget.destroy()
        with open("varlik.json", "r") as d:
            global birim_sayisi
            birim_sayisi -= 8
            veri_deneme = json.load(d)
            with open("corrected-Result.json", "r") as cr:
                cr_veri = json.load(cr)
                if birim_sayisi<8:
                    birim_sayisi += 8
                keys_list = list(veri_deneme.keys())
                for key in keys_list:
                    values = []
                    inside_keys = list(veri_deneme[key].keys())
                    for inside_key in inside_keys:
                        values.append(veri_deneme[key][inside_key]["Miktar"])
                    toplamyy = float("{:.2f}".format(sum(values)))
                    if toplamyy <= 0:
                        keys_list.remove(key)
                keys_list.sort()
                for key in keys_list[birim_sayisi-8:birim_sayisi]:
                    values = []
                    inside_keys = list(veri_deneme[key].keys())
                    for inside_key in inside_keys:
                        values.append(veri_deneme[key][inside_key]["Miktar"])
                    toplamy = float("{:.2f}".format(sum(values)))
                    for keys in list(cr_veri["conversion_rates"].keys()):
                        if keys == key:
                            toplamt = (toplamy*cr_veri["conversion_rates"][key])
                            if toplamy > 0:
                                lb = Label(frtop, text="{} {}\n{:.2f}TL".format(float("{:.1f}".format(toplamy)),key,toplamt), width=8, height=3, bg="#4C4C6D", highlightcolor="grey", border=2, relief="raised",foreground="#FFE194")
                                lb.pack(side="left",padx=3)                 

    def frtop_bt_right_func():
        for widget in frtop.winfo_children():
            if isinstance(widget, Label):
                widget.destroy()
        with open("varlik.json", "r") as d:
            global birim_sayisi
            birim_sayisi += 8
            veri_deneme = json.load(d)
            with open("corrected-Result.json", "r") as cr:
                cr_veri = json.load(cr)
                keys_list = list(veri_deneme.keys())
                for key in keys_list:
                    values = []
                    inside_keys = list(veri_deneme[key].keys())
                    for inside_key in inside_keys:
                        values.append(veri_deneme[key][inside_key]["Miktar"])
                    toplamyy = float("{:.2f}".format(sum(values)))
                    if toplamyy <= 0:
                        keys_list.remove(key)
                keys_list.sort()
                if birim_sayisi >= len(keys_list)+8:
                    birim_sayisi -= 8
                for key in keys_list[birim_sayisi-8:birim_sayisi]:
                    values = []
                    inside_keys = list(veri_deneme[key].keys())
                    for inside_key in inside_keys:
                        values.append(veri_deneme[key][inside_key]["Miktar"])
                    toplamy = float("{:.2f}".format(sum(values)))
                    for keys in list(cr_veri["conversion_rates"].keys()):
                        if keys == key:
                            toplamt = (toplamy*cr_veri["conversion_rates"][key])
                            if toplamy > 0:
                                lb = Label(frtop, text="{} {}\n{:.2f}TL".format(float("{:.1f}".format(toplamy)),key,toplamt), width=8, height=3, bg="#4C4C6D", highlightcolor="grey", border=2, relief="raised",foreground="#FFE194")
                                lb.pack(side="left",padx=3)

    def sahip_olunan_birimler():
        for widget in frtop.winfo_children():
                if isinstance(widget, Label):
                    widget.destroy()
        with open("varlik.json", "r") as d:
            global birim_sayisi
            birim_sayisi = 8
            try:
                veri_deneme = json.load(d)
                with open("corrected-Result.json", "r") as cr:
                    cr_veri = json.load(cr)
                    keys_list = list(veri_deneme.keys())
                    for keys in keys_list:
                        inside_keys = list(veri_deneme[keys].keys())
                        values = []
                        for inside_key in inside_keys:
                            values.append(float(veri_deneme[keys][inside_key]["Miktar"]))
                        toplamyy = float("{:.2f}".format(sum(values)))
                        if toplamyy <= 0:
                            keys_list.remove(keys)
                    keys_list.sort()
                    if len(keys_list) > 8:
                        for key in keys_list[birim_sayisi-8:birim_sayisi]:
                            value = []
                            inside_keys = list(veri_deneme[key].keys())
                            for inside_key in inside_keys:
                                value.append(veri_deneme[key][inside_key]["Miktar"])
                            toplamy = sum(value)
                            for keys in list(cr_veri["conversion_rates"].keys()):
                                if keys == key:
                                    toplamt = (toplamy*cr_veri["conversion_rates"][key])
                                    lb = Label(frtop, text="{} {}\n{:.2f}TL".format(float("{:.1f}".format(toplamy)),key,toplamt), width=8, height=3, bg="#4C4C6D", highlightcolor="grey", border=2, relief="raised",foreground="#FFE194")
                                    lb.pack(side="left",padx=3)
                    else:
                        for key in keys_list:
                            value = []
                            inside_keys = list(veri_deneme[key].keys())
                            for inside_key in inside_keys:
                                value.append(veri_deneme[key][inside_key]["Miktar"])
                            toplamy = sum(value)
                            for keys in list(cr_veri["conversion_rates"].keys()):
                                if keys == key:
                                    toplamt = (toplamy*cr_veri["conversion_rates"][key])
                                    if toplamy > 0:
                                        lb = Label(frtop, text="{} {}\n{:.2f}TL".format(float("{:.1f}".format(toplamy)),key,toplamt), width=8, height=3, bg="#4C4C6D", highlightcolor="grey", border=2, relief="raised",foreground="#FFE194")
                                        lb.pack(side="left",padx=3)
            except:
                pass
            
    def make_own_curreny_label_satin_al():
            for widget in satin_al_frame.winfo_children():
                if isinstance(widget, Label):
                    widget.destroy()
            try:
                if float(ent.get()) == 0.0:
                    uyari = Tk()
                    uyari.geometry("210x50")
                    uyari.title("UYARI")
                    mesaj = Label(uyari, text="Miktar 0 Olamaz!")
                    bt1 = Button(uyari, text="Kapat", command=lambda:uyari.destroy())
                    mesaj.pack()
                    bt1.pack()
                    uyari.mainloop()
                else:
                    lbl = Label(satin_al_frame, text="Ekleme işlemi tamamlanmıştır.")
                    lbl1 = Label(satin_al_frame, text=f"{float(ent.get())} {lsb.selection_get()}")
                    lbl.pack(side="top")
                    lbl1.pack(side="top")
                    guncel = BooleanVar
                    dirlist = os.listdir()
                    result_list = []
                    for dr in dirlist:
                        if dr.startswith("Result"):
                            result_list.append(dr)
                    if not str(datetime.date.today()) == result_list[-1][8:18]:
                        guncel = False
                    if guncel == False:
                        from result_correction import correction
                        from API_Request import requesting
                        requesting()
                        correction()
                        frmid_tarih()
                    with open("varlik.json", "r+") as d:
                        with open("corrected-Result.json", "r") as cr:
                            veri_cr = json.load(cr)
                            kur = veri_cr["conversion_rates"][lsb.selection_get()[0:3]]
                            try:
                                veri_deneme = json.load(d)
                                if str(lsb.selection_get()[0:3]) in list(veri_deneme.keys()):
                                    veri_deneme[str(lsb.selection_get()[0:3])][str(datetime.datetime.now())] = {}
                                    veri_deneme[str(lsb.selection_get()[0:3])][str(datetime.datetime.now())]["Miktar"] = float(ent.get())
                                    veri_deneme[str(lsb.selection_get()[0:3])][str(datetime.datetime.now())]["Deger"] = kur
                                    d.seek(0)
                                    json.dump(veri_deneme, d, indent=4)
                                else:
                                    d.seek(0)
                                    veri_deneme[str(lsb.selection_get()[0:3])] = {}
                                    veri_deneme[str(lsb.selection_get()[0:3])][str(datetime.datetime.now())] = {}
                                    veri_deneme[str(lsb.selection_get()[0:3])][str(datetime.datetime.now())]["Miktar"] = float(ent.get())
                                    veri_deneme[str(lsb.selection_get()[0:3])][str(datetime.datetime.now())]["Deger"] = kur
                                    json.dump(veri_deneme, d, indent=4)
                                    d.truncate()
                            except json.decoder.JSONDecodeError:
                                kur_yazici = {f"{str(lsb.selection_get()[0:3])}": {f"{str(datetime.datetime.now())}": {"Miktar": float(ent.get()), "Deger": kur}}}
                                json.dump(kur_yazici, d, indent=4)
                    sahip_olunan_birimler()
                    frtop_right_Label()
            except ValueError:
                uyari = Tk()
                uyari.geometry("210x50")
                uyari.title("UYARI")
                mesaj = Label(uyari, text="GEÇERSİZ MİKTAR!")
                bt1 = Button(uyari, text="Kapat", command=lambda:uyari.destroy())
                mesaj.pack()
                bt1.pack()
                uyari.mainloop()
            except tkinter.TclError:
                uyari = Tk()
                uyari.geometry("210x50")
                uyari.title("UYARI")
                mesaj = Label(uyari, text="PARA BİRİMİ SEÇİLMELİDİR!")
                bt1 = Button(uyari, text="Kapat", command=lambda:uyari.destroy())
                mesaj.pack()
                bt1.pack()
                uyari.mainloop()

    def make_own_currency_label():
        global currencies
        currencies = Tk()
        currencies.geometry("380x300")
        currencies.title("EKLE")
        listbox_frame = Frame(currencies, width=0)
        listbox_frame.pack(side="left", padx=0)
        listbox_frame.propagate(False)
        listbox_frame_scroll = Scrollbar(currencies, orient="vertical")
        global lsb
        with open("corrected-Result.json", "r") as f:
            veri = json.load(f)
            lsb = Listbox(currencies, font=25,height=300)
            lsb.pack(side="left", anchor=NW)
            for key in list(veri["conversion_rates"].keys()):
                if not key == "TRY":
                    lsb.insert(END, "{}: {:.2f} TL".format(key, veri["conversion_rates"][key]))
        listbox_frame_scroll.pack(side="left",fill="y")
        listbox_frame_scroll.config(command=lsb.yview)
        lsb.config(yscrollcommand=listbox_frame_scroll.set)
        ent_lbl = Label(currencies, text="Miktar Giriniz")
        ent_lbl.pack(pady=0)
        global ent
        ent = Entry(currencies)
        ent.insert(END, 0)
        ent.pack(pady=0)
        bt1 = Button(currencies,text="EKLE",command=make_own_curreny_label_satin_al)
        bt1.pack(pady=10)
        global satin_al_frame
        satin_al_frame = Frame(currencies,width=200, height=200)
        satin_al_frame.pack(expand=0,side="right",padx=2)
        satin_al_frame.propagate(False)
        currencies.mainloop()

    def delete_own_currency_label():
        global currencies
        currencies = Tk()
        currencies.geometry("300x300")
        currencies.title("ÇIKAR")
        global lsb
        with open("varlik.json", "r") as f:
            veri = json.load(f)
            lsb = Listbox(currencies, font=25,height=300)
            lsb.pack(side="left", anchor=NW)
            keys = list(veri.keys())
            keys.sort()
            for key in keys:
                inside_keys = list(veri[key].keys())
                values = []
                for inside_key in inside_keys:
                    values.append(veri[key][inside_key]["Miktar"])
                if float("{:.2f}".format(sum(values))) > 0:
                    lsb.insert(END, "{}: {}".format(key, float("{:.2f}".format(sum(values)))))
        ent_lbl = Label(currencies, text="Miktar Giriniz")
        ent_lbl.pack(pady=0)
        global ent
        ent = Entry(currencies)
        ent.insert(END, 0)
        ent.pack(pady=0)
        bt1 = Button(currencies,text="Sat",command=delete_own_currency_label_sat)
        bt1.pack(pady=10)
        global sat_frame
        sat_frame = Frame(currencies)
        sat_frame.pack(side="right", expand=0)
        sat_frame.propagate(False)
        currencies.mainloop()

    def delete_own_currency_label_sat():
        for widget in sat_frame.winfo_children():
                if isinstance(widget, Label):
                    widget.destroy()
        try:
            if float(ent.get()) == 0 or lsb.selection_get()[0:3] == "_tkinter.TclError":
                uyari = Tk()
                uyari.geometry("210x50")
                uyari.title("UYARI")
                mesaj = Label(uyari, text="Miktar 0 Olamaz!")
                bt1 = Button(uyari, text="Kapat", command=lambda:uyari.destroy())
                mesaj.pack()
                bt1.pack()
                uyari.mainloop()
            else:
                lbl = Label(sat_frame, text="Satma işlemi tamamlanmıştır.")
                lbl1 = Label(sat_frame, text=f"{float(ent.get())} {lsb.selection_get()[0:3]}")
                lbl.pack(side="top")
                lbl1.pack(side="top")
                with open("varlik.json", "r+") as d:
                    with open("corrected-Result.json") as cr:
                        cr_veri = json.load(cr)
                        kur = cr_veri["conversion_rates"][str(lsb.selection_get()[0:3])]
                    guncel = BooleanVar
                    dirlist = os.listdir()
                    result_list = []
                    for dr in dirlist:
                        if dr.startswith("Result"):
                            result_list.append(dr)
                    if not str(datetime.date.today()) == result_list[-1][8:18]:
                        guncel = False
                    if guncel == False:
                        from result_correction import correction
                        from API_Request import requesting
                        requesting()
                        correction()
                        frmid_tarih()
                    veri_deneme = json.load(d)
                    try:
                        values = []
                        inside_keys = list(veri_deneme[str(lsb.selection_get()[0:3])].keys())
                        for inside_key in inside_keys:
                            values.append(veri_deneme[str(lsb.selection_get()[0:3])][inside_key]["Miktar"])
                        if float(ent.get()) > sum(values):
                            raise ValueError
                    except ValueError:
                        uyari = Tk()
                        uyari.geometry("210x50")
                        uyari.title("UYARI")
                        mesaj = Label(uyari, text="BU MİKTAR SATILAMAZ!")
                        bt1 = Button(uyari, text="Kapat", command=lambda:uyari.destroy())
                        mesaj.pack()
                        bt1.pack()
                        uyari.mainloop()
                    veri_deneme[str(lsb.selection_get()[0:3])][str(datetime.datetime.now())] = {}
                    veri_deneme[str(lsb.selection_get()[0:3])][str(datetime.datetime.now())]["Miktar"] = -abs(float(ent.get()))
                    veri_deneme[str(lsb.selection_get()[0:3])][str(datetime.datetime.now())]["Deger"] = float(kur)
                    d.seek(0)
                    json.dump(veri_deneme, d, indent=4)
                sahip_olunan_birimler()
                frtop_right_Label()
        except ValueError:
            uyari = Tk()
            uyari.geometry("210x50")
            uyari.title("UYARI")
            mesaj = Label(uyari, text="GEÇERSİZ MİKTAR!")
            bt1 = Button(uyari, text="Kapat", command=lambda:uyari.destroy())
            mesaj.pack()
            bt1.pack()
            uyari.mainloop()
        except tkinter.TclError:
            uyari = Tk()
            uyari.geometry("210x50")
            uyari.title("UYARI")
            mesaj = Label(uyari, text="PARA BİRİMİ SEÇİLMELİDİR!")
            bt1 = Button(uyari, text="Kapat", command=lambda:uyari.destroy())
            mesaj.pack()
            bt1.pack()
            uyari.mainloop()

    def en_degerli_kur():
        try:
            with open("varlik.json") as d:
                d_veri = json.load(d)
                en_buyuk_kur = StringVar
                en_buyuk_deger = 0
                kurlar = list(d_veri.keys())
                for kur in kurlar:
                    tarihler = list(d_veri[kur].keys())
                    toplam = 0
                    for tarih in tarihler:
                        toplam += round(d_veri[kur][tarih]["Miktar"])
                    if toplam * d_veri[kur][tarih]["Deger"] >= en_buyuk_deger:
                        en_buyuk_deger = toplam * d_veri[kur][tarih]["Deger"]
                        en_buyuk_kur = kur
        except:
            return 0
        return en_buyuk_kur

    def graphs(kur):
        try:
            with open("varlik.json") as d:
                d_veri = json.load(d)
                rate = d_veri[kur]
                x = []
                y_yabanci_temp = []
                y_turk = []
                y_yabanci = []
                renk_toplami = 0
                for date in list(rate.keys()):
                    if x.count(date[:10]) < 1:
                        x.append(date[:10])
                    if date.startswith(x[0]):
                        renk_toplami += round(rate[date]["Miktar"])*round(rate[date]["Deger"])
                for x_date in x:
                    y_yabanci_temp.append(0)
                    for kur_date in list(rate.keys()):
                        if kur_date.startswith(x_date):
                            y_yabanci_temp[len(y_yabanci_temp)-1] += round(rate[kur_date]["Miktar"])
                if str(datetime.date.today()) != x[-1]:
                    x.append(str(datetime.date.today()))
                    y_yabanci_temp.append(0)
                for value in y_yabanci_temp:
                    y_yabanci.append(value)
                    y_yabanci_toplam = sum(y_yabanci_temp[:len(y_yabanci)])
                    y_yabanci.pop()
                    y_yabanci.append(y_yabanci_toplam)
                    y_turk.append(value)
                    y_turk_toplam = sum(y_yabanci_temp[:len(y_turk)])
                    y_turk.pop()
                    y_turk.append(y_turk_toplam)
                dirlist = os.listdir()
                result_list = []
                for dr in dirlist:
                    if dr.startswith("Result"):
                        result_list.append(dr)
                if result_list[-1][8:18] != str(datetime.date.today()):
                    from API_Request import requesting
                    from result_correction import correction
                    requesting()
                    time.sleep(1)
                    correction()
                index = 0
                for x_date in x:
                    if x_date == x[-1]:
                        with open("corrected-Result.json") as cr:
                            veri_cr = json.load(cr)
                            kur_deger = veri_cr["conversion_rates"][kur]
                            y_turk[index] *= kur_deger
                    else:
                        for result in result_list:
                            if result[8:18] == x_date:
                                with open(result) as rs:
                                    rs_veri = json.load(rs)
                                    y_turk[index] *= round(1/rs_veri["conversion_rates"][kur])
                    index += 1
                if y_turk[-1] > renk_toplami:
                    c = "green"
                elif y_turk[-1] == renk_toplami:
                    c = "grey"
                else:
                    c = "red"
            fig = Figure(figsize=(5, 4), dpi=100)
            ax1 = fig.add_subplot(211)
            ax1.plot(x,y_yabanci,c = "blue")
            ax1.grid()
            ax1.set_title(kur,color="#FFE194")
            ax1.set_xticks(x)
            ax1.set_yticks(y_yabanci)
            ax1.tick_params(axis="both",colors="#FFE194")
            ax2 = fig.add_subplot(212)
            ax2.plot(x,y_turk,c = c)
            ax2.grid()
            ax2.set_title("{}(TRY)".format(kur),color="#FFE194")
            ax2.set_xticks(x)
            ax2.set_yticks(y_turk)
            ax2.tick_params(axis="both",colors="#FFE194")
            fig.subplots_adjust(hspace=0.7,left=0.12)
            fig.set_facecolor("#4C4C6D")
            fig.set_figwidth(550)
            return fig
        except:
            return 0

    def graphs_canvas(str=en_degerli_kur()):
        try:
            for children in frmid.winfo_children():
                if isinstance(children, Canvas):
                    children.destroy()
            canvas = FigureCanvasTkAgg(graphs(str), master=frmid)
            canvas.draw()
            canvas.get_tk_widget().config(background="#4C4C6D")
            canvas.get_tk_widget().pack(fill="both")
        except:
            return 0

    def kur_seç():
        global currencies
        currencies = Tk()
        currencies.geometry("300x300")
        currencies.title("Sat")
        global lsb_seç
        with open("varlik.json", "r") as f:
            veri = json.load(f)
            lsb_seç = Listbox(currencies, font=25,height=300)
            lsb_seç.pack(side="left", anchor=NW)
            keys = list(veri.keys())
            keys.sort()
            for key in keys:
                inside_keys = list(veri[key].keys())
                values = []
                for inside_key in inside_keys:
                    values.append(veri[key][inside_key]["Miktar"])
                lsb_seç.insert(END, "{}: {}".format(key, float("{:.2f}".format(sum(values)))))
        bt1 = Button(currencies,text="Seç", command=kur_seç_buton_seç)
        bt1.pack(pady=125)
        global sat_frame
        sat_frame = Frame(currencies)
        sat_frame.pack(side="right", expand=0)
        sat_frame.propagate(False)
        currencies.mainloop()

    def kur_seç_buton_seç():
        kur = str(lsb_seç.selection_get()[0:3])
        graphs_canvas(kur)
        currencies.destroy()

    def kur_durumlari():
        for children in frmid.winfo_children():
            if isinstance(children, Canvas):
                children.destroy()
        try:
            kur = str(frright_listbox.selection_get()[:3])
        except tkinter.TclError:
            pass
        else:
            dirlist = os.listdir()
            result_list = []
            for dr in dirlist:
                if dr.startswith("Result"):
                    result_list.append(dr)
            x = []
            y = []    
            for result in result_list:
                x.append(result[8:18])
                with open(result) as rs:
                    rs_veri = json.load(rs)
                    if kur == "GrA" or kur == "CrA" or kur == "YrA" or kur == "TmA":
                        y.append(round(1/rs_veri["conversion_rates"][kur],3))
                    else:
                        y.append(round(1/round(rs_veri["conversion_rates"][kur], 3),3))
            if y[-1] > y[0]:
                c = "green"
            elif y[-1] == y[0]:
                c = "grey"
            else:
                c = "red"
            fig = Figure(figsize=(5, 4), dpi=100)
            ax1 = fig.add_subplot(111)
            ax1.plot(x,y,c = c)
            ax1.grid()
            ax1.set_title(kur,color="#FFE194")
            ax1.set_xticks(x)
            ax1.set_yticks(y)
            ax1.tick_params(axis="both",colors="#FFE194")
            fig.subplots_adjust(hspace=0.7,left=0.12)
            fig.set_facecolor("#4C4C6D")
            fig.set_figwidth(550)
            canvas = FigureCanvasTkAgg(fig, master=frmid)
            canvas.draw()
            canvas.get_tk_widget().config(background="#4C4C6D")
            canvas.get_tk_widget().pack(fill="both")


    pen = Tk()
    pen.configure(bg="#4C4C6D")
    pen.geometry("800x600")
    pen.resizable(0,0)

    # Sol Frame
    frleft = Frame(pen,bg="#202020", width=50, height=800)
    frleft.pack(side="left")
    frleft.propagate(False)
    frleft_bt1 = Button(frleft, text="Yenile", command=frleft_yenile_buton, height=2)
    frleft_bt1.pack(side="top", fill="both")
    frleft_bt2 = Button(frleft, text="ÇIK", command=lambda: pen.destroy(), height=2)
    frleft_bt2.pack(side="bottom", fill="x")

    # Üst Frame
    frtop = Frame(pen, bg="#FFE194", width=800, height=100, relief="ridge", border=5)
    frtop.pack(side="top", expand=1,fill="both")
    frtop.propagate(False)
    frtop_right = Frame(frtop, bg="#FFD494", width=150, height=100,relief="ridge", border=5)
    frtop_right.pack(side="right")
    frtop_right.propagate(False)
    frtop_bt_left = Button(frtop, text="Geri", command=frtop_bt_left_func)
    frtop_bt_left.pack(side="left")
    frtop_bt_right = Button(frtop, text="İleri", command=frtop_bt_right_func)
    frtop_bt_right.pack(side="right")

    sahip_olunan_birimler()
    frtop_right_Label()

    # Sağ Frame
    frright = Frame(pen, bg="#4C4C60", width=150, height=800, relief="sunken", border=5)
    frright.pack(side="right")
    frright.propagate(False)
    frright_top_frame = Frame(frright, bg="#4C4C60")
    frright_top_frame.pack(side="top")
    frright_bt1 = Button(frright_top_frame, text="EKLE", command=make_own_currency_label)
    frright_bt1.pack(side="left", padx=7)
    frright_bt2 = Button(frright_top_frame, text="ÇIKAR", command=delete_own_currency_label)
    frright_bt2.pack(side="right", padx=7)
    frright_scroll = Scrollbar(frright, orient="vertical",bg="#4C4C60")
    frright_scroll.pack(side="right", fill="y")

    try:
        with open("corrected-Result.json", "r") as f:
            veri = json.load(f)
            frright_listbox = Listbox(frright, width=100, height=300, font=25, selectbackground="white",selectforeground="black", bg="white")
            frright_listbox.pack(side="left")
            for key in list(veri["conversion_rates"].keys()):
                if not key == "TRY":
                    frright_listbox.insert(END, "{}: {:.3f}".format(key, veri["conversion_rates"][key]))
            frright_listbox.config(yscrollcommand=frright_scroll.set)
            frright_scroll.config(command=frright_listbox.yview)
    except:
        pass

    # Orta Frame
    frmid = Frame(pen, bg="#4C4C6D",height=500, relief="sunken", border=5)
    frmid.pack(fill="both")
    frmid.propagate(False)
    frmid_top_left_frame = Frame(frmid, bg="#4C4C6D")
    frmid_top_left_frame.pack(side="top",fill="x")
    frmid_top_left_label = Label(frmid_top_left_frame, text=frmid_tarih(), bg="#4C4C6D", foreground="white")
    frmid_top_left_label.pack(side="left", anchor=W, padx=5,pady=5)
    frmid_top_right_button = Button(frmid_top_left_frame, text="Varlık Grafiği Seç", command=kur_seç)
    frmid_top_right_button.pack(side="right", anchor=E, padx=5, pady=5)
    frmid_top_right_secondbutton = Button(frmid_top_left_frame, text="Grafik Yenile", command=restart_program)
    frmid_top_right_secondbutton.pack(side="right",anchor=E,padx=5,pady=5)
    frmid_bottom_right_button = Button(frmid, text="Kur Seç", command=kur_durumlari)
    frmid_bottom_right_button.pack(side="bottom",anchor=E,padx=5,pady=5)

    dikkat = Label(frmid,text="LÜTFEN 'KUR SEÇ' BUTONUNA TIKLAMADAN ÖNCE SAĞ SEKMEDEN BİR KUR SEÇİNİZ.", bg="#4C4C6D")
    dikkat.pack(side=BOTTOM,anchor=E)
    
    dirlist = os.listdir()
    popup_bool = False
    for dr in dirlist:
        if dr.startswith("Result"):
            popup_bool = True
    
    if popup_bool == False:
        tkinter.messagebox.showinfo(title="Uyarı", message="Lütfen İlk Önce 'YENİLE' Butonuna Tıklayınız.")
    
    graphs_canvas()
    pen.mainloop()
except:
    os.system("pip install matplotlib")
    os.system("pip install requests")
    os.system("pip install json")
    os.system("pip install http.client")
    os.system("pip install tkinter")
    os.execv(sys.executable, ['python'] + sys.argv)