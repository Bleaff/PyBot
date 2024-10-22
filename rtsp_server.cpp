#include <boost/asio.hpp>
#include <iostream>
#include <string>

using boost::asio::ip::tcp;

class RTSP_Server {
public:
    RTSP_Server(boost::asio::io_service& io_service, short port)
        : acceptor_(io_service, tcp::endpoint(tcp::v4(), port)) {
        start_accept();
    }

private:
    void start_accept() {
        tcp::socket socket_(acceptor_.get_io_service());
        acceptor_.async_accept(socket_,
            [this, socket = std::move(socket_)](const boost::system::error_code& error) mutable {
                if (!error) {
                    std::make_shared<RTSP_Session>(std::move(socket))->start();
                }
                start_accept();
            });
    }

    tcp::acceptor acceptor_;
};

class RTSP_Session : public std::enable_shared_from_this<RTSP_Session> {
public:
    RTSP_Session(tcp::socket socket)
        : socket_(std::move(socket)) {}

    void start() {
        do_read();
    }

private:
    void do_read() {
        auto self(shared_from_this());
        boost::asio::async_read_until(socket_, buffer_, "\r\n\r\n",
            [this, self](const boost::system::error_code& ec, std::size_t length) {
                if (!ec) {
                    std::istream request_stream(&buffer_);
                    std::string request;
                    std::getline(request_stream, request);
                    if (request.find("OPTIONS") == 0) {
                        handle_options();
                    } else if (request.find("DESCRIBE") == 0) {
                        handle_describe();
                    } else if (request.find("SETUP") == 0) {
                        handle_setup();
                    } else if (request.find("PLAY") == 0) {
                        handle_play();
                    }
                    do_read();
                }
            });
    }

    void handle_options() {
        std::string response =
            "RTSP/1.0 200 OK\r\n"
            "CSeq: 1\r\n"
            "Public: OPTIONS, DESCRIBE, SETUP, PLAY\r\n\r\n";
        do_write(response);
    }

    void handle_describe() {
        std::string response =
            "RTSP/1.0 200 OK\r\n"
            "CSeq: 2\r\n"
            "Content-Base: rtsp://localhost/\r\n"
            "Content-Type: application/sdp\r\n"
            "Content-Length: 95\r\n\r\n"
            "v=0\r\n"
            "o=- 0 0 IN IP4 127.0.0.1\r\n"
            "s=No Name\r\n"
            "c=IN IP4 127.0.0.1\r\n"
            "t=0 0\r\n"
            "a=tool:libavformat 58.29.100\r\n"
            "m=video 0 RTP/AVP 96\r\n"
            "a=rtpmap:96 H264/90000\r\n";
        do_write(response);
    }

    void handle_setup() {
        std::string response =
            "RTSP/1.0 200 OK\r\n"
            "CSeq: 3\r\n"
            "Transport: RTP/AVP;unicast;client_port=8000-8001\r\n"
            "Session: 12345678\r\n\r\n";
        do_write(response);
    }

    void handle_play() {
        std::string response =
            "RTSP/1.0 200 OK\r\n"
            "CSeq: 4\r\n"
            "Session: 12345678\r\n\r\n";
        do_write(response);
    }

    void do_write(const std::string& response) {
        auto self(shared_from_this());
        boost::asio::async_write(socket_, boost::asio::buffer(response),
            [this, self](const boost::system::error_code& ec, std::size_t /*length*/) {
                if (!ec) {
                    // Write completed
                }
            });
    }

    tcp::socket socket_;
    boost::asio::streambuf buffer_;
};