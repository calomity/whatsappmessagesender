package main

import (
	"encoding/gob"
	"fmt"
	qrcodeTerminal "github.com/Baozisoftware/qrcode-terminal-go"
	"github.com/Rhymen/go-whatsapp"
	"os"
	"time"
)

func writeSession(session whatsapp.Session) error {
	file, err := os.Create(os.TempDir() + "/whatsappSession.gob")
	if err != nil {
		return err
	}
	defer file.Close()
	encoder := gob.NewEncoder(file)
	err = encoder.Encode(session)
	if err != nil {
		return err
	}
	return nil
}

func readSession() (whatsapp.Session, error) {
	session := whatsapp.Session{}
	file, err := os.Open(os.TempDir() + "/whatsappSession.gob")
	if err != nil {
		return session, err
	}
	defer file.Close()
	decoder := gob.NewDecoder(file)
	err = decoder.Decode(&session)
	if err != nil {
		return session, err
	}
	return session, nil
}

func login(wac *whatsapp.Conn) error{
	session, err := readSession()
	if err == nil{
		session, err = wac.RestoreWithSession(session)
		if err != nil {
			return fmt.Errorf("restoring failed: %v\n", err)
		}
	} else {
		qr := make(chan string)
		go func(){
			terminal := qrcodeTerminal.New()
			terminal.Get(<-qr).Print()
		}()
		session, err = wac.Login(qr)
		if err != nil {
			return fmt.Errorf("error during login: %v\n", err)
		}
	}
	err = writeSession(session)
	if err != nil {
		return fmt.Errorf("error saving session: %v\n", err)
	}
	return nil
}

func main(){
	_ = os.Args[2]
	telno := os.Args[1]
	message := os.Args[2]
	fmt.Println("Telefon numarası(ları): ", telno, "\n")
	fmt.Println("Gönderilen Mesaj: ", message, "\n")

	wac, err := whatsapp.NewConn(2 * time.Second)
	wac.SetClientVersion(2, 2123, 7)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Bağlantı sırasında hata: %v\n", err)
		return
	}

	err = login(wac)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Giriş sırasında hata: %v\n", err)
		return
	}

	text := whatsapp.TextMessage{
		Info: whatsapp.MessageInfo{
			RemoteJid: telno + "@s.whatsapp.net",
		},
		Text: message,
	}

	msginfo, err := wac.Send(text)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Mesaj gönderiminde bir sıkıntı oldu: %v", err)
	} else {
		fmt.Println("Mesaj(lar) başarıyla gönderilmiştir\n")
		fmt.Println("Mesaj ID(leri) : " + msginfo)
	}
}